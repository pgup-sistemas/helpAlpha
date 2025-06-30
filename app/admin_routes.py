from flask import render_template, request, redirect, url_for, flash, jsonify, current_app, send_file
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, PasswordResetToken, Exame, Unidade, Aviso, LogAcesso, EstatisticaExame, EstatisticaBusca, SiteConfig
from app.extensions import db
from app.forms import LoginForm, ExameForm, UploadExcelForm, PasswordResetRequestForm, PasswordResetForm, UnidadeForm, AvisoForm, SiteConfigForm, UserForm
from app.security import PermissionHelper
import json
import os
import pandas as pd
import math
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

# Tentar importar matplotlib (opcional)
try:
    import matplotlib
    matplotlib.use('Agg')  # Backend não-interativo
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    plt = None
    sns = None

from io import BytesIO
import base64
from sqlalchemy import func, desc

# Importar decoradores de rate limiting
try:
    from app.rate_limiting import (
        login_rate_limit, upload_rate_limit, admin_rate_limit, 
        reset_password_rate_limit
    )
except ImportError:
    # Fallback se o rate limiting não estiver disponível
    def login_rate_limit(f): return f
    def upload_rate_limit(f): return f
    def admin_rate_limit(f): return f
    def reset_password_rate_limit(f): return f

# Obter o diretório base do aplicativo
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_ROOT)

def register_admin_routes(app):
    """Registra as rotas administrativas"""
    
    @app.route('/admin/login', methods=['GET', 'POST'])
    @login_rate_limit
    def admin_login():
        """Login administrativo"""
        if current_user.is_authenticated:
            return redirect(url_for('admin_dashboard'))
        
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data) and user.is_active:
                login_user(user)
                user.last_login = db.func.now()
                user.update_activity()
                db.session.commit()
                
                next_page = request.args.get('next')
                if not next_page or not next_page.startswith('/'):
                    next_page = url_for('admin_dashboard')
                return redirect(next_page)
            else:
                flash('Usuário ou senha inválidos!', 'danger')
        
        return render_template('admin/login.html', form=form)

    @app.route('/admin/logout')
    @login_required
    def admin_logout():
        """Logout administrativo"""
        logout_user()
        flash('Você foi desconectado com sucesso!', 'info')
        return redirect(url_for('admin_login'))

    @app.route('/admin/reset-password', methods=['GET', 'POST'])
    @reset_password_rate_limit
    def admin_reset_password_request():
        """Solicitar redefinição de senha"""
        form = PasswordResetRequestForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.is_active:
                token = user.generate_reset_token()
                flash(f'Token de redefinição gerado: {token}', 'info')
                flash('Use este token para redefinir sua senha. O token é válido por 24 horas.', 'warning')
                return redirect(url_for('admin_reset_password', token=token))
            else:
                flash('Usuário não encontrado ou inativo!', 'danger')
        
        return render_template('admin/reset_password_request.html', form=form)

    @app.route('/admin/reset-password/<token>', methods=['GET', 'POST'])
    @reset_password_rate_limit
    def admin_reset_password(token):
        """Redefinir senha com token"""
        reset_token = PasswordResetToken.query.filter_by(token=token).first()
        
        if not reset_token or not reset_token.is_valid():
            flash('Token inválido ou expirado!', 'danger')
            return redirect(url_for('admin_reset_password_request'))
        
        form = PasswordResetForm()
        if form.validate_on_submit():
            user = reset_token.user
            user.set_password(form.password.data)
            reset_token.mark_as_used()
            db.session.commit()
            
            flash('Senha redefinida com sucesso!', 'success')
            return redirect(url_for('admin_login'))
        
        return render_template('admin/reset_password.html', form=form, token=token)

    @app.route('/admin')
    @login_required
    def admin_dashboard():
        """Dashboard administrativo"""
        current_user.update_activity()
        
        # Estatísticas básicas
        total_exames = Exame.query.count()
        total_unidades = Unidade.query.filter_by(is_ativo=True).count()
        total_avisos = Aviso.query.filter_by(is_ativo=True).count()
        total_usuarios = User.query.count()
        
        # Últimos acessos
        acessos_recentes = LogAcesso.query.order_by(LogAcesso.created_at.desc()).limit(10).all()
        
        # Usuários ativos recentemente
        usuarios_ativos = User.query.filter(
            User.last_activity >= datetime.utcnow() - timedelta(days=7)
        ).order_by(User.last_activity.desc()).limit(5).all()
        
        return render_template('admin/dashboard.html',
                             total_exames=total_exames,
                             total_unidades=total_unidades,
                             total_avisos=total_avisos,
                             total_usuarios=total_usuarios,
                             acessos_recentes=acessos_recentes,
                             usuarios_ativos=usuarios_ativos)

    @app.route('/admin/exames')
    @login_required
    def admin_exames():
        """Lista de exames no painel administrativo"""
        page = request.args.get('page', 1, type=int)
        per_page = current_app.config.get('ADMIN_EXAMES_PER_PAGE', 9)
        
        # Filtros
        categoria = request.args.get('categoria')
        busca = request.args.get('busca')
        
        query = Exame.query
        
        if categoria:
            query = query.filter_by(categoria=categoria)
        
        if busca:
            query = query.filter(Exame.nome.ilike(f'%{busca}%'))
        
        exames = query.order_by(Exame.nome).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('admin/exames.html', exames=exames)

    @app.route('/admin/exames/add', methods=['GET', 'POST'])
    @login_required
    @PermissionHelper.require_edit_permission
    def admin_add_exame():
        """Adicionar novo exame"""
        form = ExameForm()
        
        if form.validate_on_submit():
            exame = Exame(
                nome=form.nome.data,
                descricao=form.descricao.data,
                preparo=form.preparo.data,
                documentos=form.documentos.data,
                pos_exame=form.pos_exame.data,
                tempo=form.tempo.data,
                categoria=form.categoria.data,
                icone=form.icone.data
            )
            
            db.session.add(exame)
            db.session.commit()
            
            flash('Exame adicionado com sucesso!', 'success')
            return redirect(url_for('admin_exames'))
        
        return render_template('admin/exame_form.html', form=form, title='Adicionar Exame')

    @app.route('/admin/exames/edit/<nome>', methods=['GET', 'POST'])
    @login_required
    @PermissionHelper.require_edit_permission
    def admin_edit_exame(nome):
        """Editar exame existente"""
        exame = Exame.query.filter_by(nome=nome).first_or_404()
        form = ExameForm(obj=exame)
        
        if form.validate_on_submit():
            exame.nome = form.nome.data
            exame.descricao = form.descricao.data
            exame.preparo = form.preparo.data
            exame.documentos = form.documentos.data
            exame.pos_exame = form.pos_exame.data
            exame.tempo = form.tempo.data
            exame.categoria = form.categoria.data
            exame.icone = form.icone.data
            
            db.session.commit()
            
            flash('Exame atualizado com sucesso!', 'success')
            return redirect(url_for('admin_exames'))
        
        return render_template('admin/exame_form.html', form=form, title='Editar Exame')

    @app.route('/admin/exames/delete/<nome>', methods=['POST'])
    @login_required
    @PermissionHelper.require_permission('delete')
    def admin_delete_exame(nome):
        """Deletar exame"""
        exame = Exame.query.filter_by(nome=nome).first_or_404()
        
        db.session.delete(exame)
        db.session.commit()
        
        flash('Exame deletado com sucesso!', 'success')
        return redirect(url_for('admin_exames'))

    @app.route('/admin/upload-excel', methods=['GET', 'POST'])
    @login_required
    @PermissionHelper.require_edit_permission
    @upload_rate_limit
    def admin_upload_excel():
        """Upload de arquivo Excel para adicionar exames em massa"""
        form = UploadExcelForm()
        
        if form.validate_on_submit():
            try:
                # Salvar arquivo temporariamente
                filename = secure_filename(form.arquivo.data.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                
                # Criar diretório se não existir
                os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
                
                form.arquivo.data.save(file_path)
                
                # Processar arquivo
                exames_data, error = process_excel_file(file_path)
                
                # Remover arquivo temporário
                os.remove(file_path)
                
                if error:
                    flash(f'Erro ao processar arquivo: {error}', 'danger')
                    return render_template('admin/upload_excel.html', form=form)
                
                if exames_data:
                    # Salvar no banco de dados
                    exames_adicionados = 0
                    exames_atualizados = 0
                    
                    for exame_data in exames_data:
                        exame_existente = Exame.query.filter_by(nome=exame_data['nome']).first()
                        
                        if exame_existente:
                            # Atualizar exame existente
                            exame_existente.descricao = exame_data['descricao']
                            exame_existente.preparo = exame_data['preparo']
                            exame_existente.documentos = exame_data['documentos']
                            exame_existente.pos_exame = exame_data['pos_exame']
                            exame_existente.tempo = exame_data['tempo']
                            exame_existente.categoria = exame_data.get('categoria', 'laboratorio')
                            exame_existente.icone = exame_data.get('icone', '')
                            exames_atualizados += 1
                        else:
                            # Criar novo exame
                            novo_exame = Exame(
                                nome=exame_data['nome'],
                                descricao=exame_data['descricao'],
                                preparo=exame_data['preparo'],
                                documentos=exame_data['documentos'],
                                pos_exame=exame_data['pos_exame'],
                                tempo=exame_data['tempo'],
                                categoria=exame_data.get('categoria', 'laboratorio'),
                                icone=exame_data.get('icone', '')
                            )
                            db.session.add(novo_exame)
                            exames_adicionados += 1
                    
                    db.session.commit()
                    
                    flash(f'Upload concluído! {exames_adicionados} exames adicionados e {exames_atualizados} atualizados.', 'success')
                else:
                    flash('Nenhum exame válido encontrado no arquivo.', 'warning')
                
                return redirect(url_for('admin_exames'))
                
            except Exception as e:
                flash(f'Erro ao processar arquivo: {str(e)}', 'danger')
        
        return render_template('admin/upload_excel.html', form=form)

    @app.route('/admin/download-template')
    @login_required
    def admin_download_template():
        """Download do template Excel"""
        try:
            # Criar template Excel
            template_data = {
                'Nome': ['Exame de Sangue', 'Ressonância Magnética', 'Vacina COVID-19'],
                'Descrição': ['Análise completa do sangue', 'Exame de imagem do corpo', 'Vacina contra COVID-19'],
                'Preparo': ['Jejum de 12 horas', 'Não é necessário preparo', 'Não é necessário preparo'],
                'Documentos': ['RG, CPF', 'RG, CPF, pedido médico', 'RG, CPF'],
                'Pós-exame': ['Pode retomar alimentação normal', 'Pode retomar atividades normais', 'Aguardar 15 minutos'],
                'Tempo': ['1 dia útil', '3 dias úteis', 'Imediato'],
                'Categoria': ['laboratorio', 'imagem', 'vacina'],
                'Ícone': ['fas fa-flask', 'fas fa-x-ray', 'fas fa-syringe']
            }
            
            df = pd.DataFrame(template_data)
            
            # Criar arquivo temporário
            template_path = os.path.join(current_app.config['DOWNLOAD_FOLDER'], 'template_exames.xlsx')
            os.makedirs(current_app.config['DOWNLOAD_FOLDER'], exist_ok=True)
            
            df.to_excel(template_path, index=False, engine='openpyxl')
            
            return send_file(template_path, as_attachment=True, download_name='template_exames.xlsx')
            
        except Exception as e:
            flash(f'Erro ao gerar template: {str(e)}', 'danger')
            return redirect(url_for('admin_upload_excel'))

    # ===== ROTAS PARA UNIDADES =====
    
    @app.route('/admin/unidades')
    @login_required
    def admin_unidades():
        """Lista de unidades"""
        unidades = Unidade.query.order_by(Unidade.nome).all()
        return render_template('admin/unidades.html', unidades=unidades)

    @app.route('/admin/unidades/add', methods=['GET', 'POST'])
    @login_required
    @PermissionHelper.require_edit_permission
    def admin_add_unidade():
        """Adicionar nova unidade"""
        form = UnidadeForm()
        
        if form.validate_on_submit():
            unidade = Unidade(
                nome=form.nome.data,
                endereco=form.endereco.data,
                telefones=form.telefones.data,
                horarios=form.horarios.data,
                coordenadas=form.coordenadas.data
            )
            
            db.session.add(unidade)
            db.session.commit()
            
            flash('Unidade adicionada com sucesso!', 'success')
            return redirect(url_for('admin_unidades'))
        
        return render_template('admin/unidade_form.html', form=form, title='Adicionar Unidade')

    @app.route('/admin/unidades/edit/<int:unidade_id>', methods=['GET', 'POST'])
    @login_required
    @PermissionHelper.require_edit_permission
    def admin_edit_unidade(unidade_id):
        """Editar unidade"""
        unidade = Unidade.query.get_or_404(unidade_id)
        form = UnidadeForm(obj=unidade)
        
        if form.validate_on_submit():
            unidade.nome = form.nome.data
            unidade.endereco = form.endereco.data
            unidade.telefones = form.telefones.data
            unidade.horarios = form.horarios.data
            unidade.coordenadas = form.coordenadas.data
            
            db.session.commit()
            
            flash('Unidade atualizada com sucesso!', 'success')
            return redirect(url_for('admin_unidades'))
        
        return render_template('admin/unidade_form.html', form=form, title='Editar Unidade')

    @app.route('/admin/unidades/delete/<int:unidade_id>', methods=['POST'])
    @login_required
    @PermissionHelper.require_permission('delete')
    def admin_delete_unidade(unidade_id):
        """Deletar unidade"""
        unidade = Unidade.query.get_or_404(unidade_id)
        
        db.session.delete(unidade)
        db.session.commit()
        
        flash('Unidade deletada com sucesso!', 'success')
        return redirect(url_for('admin_unidades'))

    # ===== ROTAS PARA AVISOS =====
    
    @app.route('/admin/avisos')
    @login_required
    def admin_avisos():
        """Lista de avisos"""
        avisos = Aviso.query.order_by(Aviso.created_at.desc()).all()
        return render_template('admin/avisos.html', avisos=avisos)

    @app.route('/admin/avisos/add', methods=['GET', 'POST'])
    @login_required
    @PermissionHelper.require_edit_permission
    def admin_add_aviso():
        """Adicionar novo aviso"""
        form = AvisoForm()
        
        if form.validate_on_submit():
            aviso = Aviso(
                titulo=form.titulo.data,
                conteudo=form.conteudo.data,
                tipo=form.tipo.data,
                is_ativo=form.is_ativo.data,
                data_inicio=form.data_inicio.data,
                data_fim=form.data_fim.data
            )
            
            db.session.add(aviso)
            db.session.commit()
            
            flash('Aviso adicionado com sucesso!', 'success')
            return redirect(url_for('admin_avisos'))
        
        return render_template('admin/aviso_form.html', form=form, title='Adicionar Aviso')

    @app.route('/admin/avisos/edit/<int:aviso_id>', methods=['GET', 'POST'])
    @login_required
    @PermissionHelper.require_edit_permission
    def admin_edit_aviso(aviso_id):
        """Editar aviso"""
        aviso = Aviso.query.get_or_404(aviso_id)
        form = AvisoForm(obj=aviso)
        
        if form.validate_on_submit():
            aviso.titulo = form.titulo.data
            aviso.conteudo = form.conteudo.data
            aviso.tipo = form.tipo.data
            aviso.is_ativo = form.is_ativo.data
            aviso.data_inicio = form.data_inicio.data
            aviso.data_fim = form.data_fim.data
            
            db.session.commit()
            
            flash('Aviso atualizado com sucesso!', 'success')
            return redirect(url_for('admin_avisos'))
        
        return render_template('admin/aviso_form.html', form=form, title='Editar Aviso')

    @app.route('/admin/avisos/delete/<int:aviso_id>', methods=['POST'])
    @login_required
    @PermissionHelper.require_permission('delete')
    def admin_delete_aviso(aviso_id):
        """Deletar aviso"""
        aviso = Aviso.query.get_or_404(aviso_id)
        
        db.session.delete(aviso)
        db.session.commit()
        
        flash('Aviso deletado com sucesso!', 'success')
        return redirect(url_for('admin_avisos'))

    @app.route('/admin/relatorios')
    @login_required
    def relatorios():
        """Página principal de relatórios"""
        return render_template('admin/relatorios.html')
    
    @app.route('/admin/relatorios/estatisticas')
    @login_required
    def estatisticas_gerais():
        """Estatísticas gerais do sistema"""
        # Estatísticas básicas
        total_exames = Exame.query.count()
        total_unidades = Unidade.query.filter_by(is_ativo=True).count()
        total_avisos = Aviso.query.filter_by(is_ativo=True).count()
        
        # Acessos hoje
        hoje = datetime.utcnow().date()
        acessos_hoje = LogAcesso.query.filter(
            func.date(LogAcesso.created_at) == hoje
        ).count()
        
        # Acessos esta semana
        inicio_semana = hoje - timedelta(days=7)
        acessos_semana = LogAcesso.query.filter(
            LogAcesso.created_at >= inicio_semana
        ).count()
        
        # Exames mais consultados (últimos 30 dias)
        inicio_mes = hoje - timedelta(days=30)
        exames_populares = db.session.query(
            Exame.nome,
            func.count(EstatisticaExame.id).label('consultas')
        ).join(EstatisticaExame).filter(
            EstatisticaExame.created_at >= inicio_mes
        ).group_by(Exame.id, Exame.nome).order_by(
            desc('consultas')
        ).limit(10).all()
        
        # Termos de busca mais populares
        termos_populares = db.session.query(
            EstatisticaBusca.termo_busca,
            func.count(EstatisticaBusca.id).label('buscas')
        ).filter(
            EstatisticaBusca.created_at >= inicio_mes
        ).group_by(EstatisticaBusca.termo_busca).order_by(
            desc('buscas')
        ).limit(10).all()
        
        # Gerar gráficos
        grafico_exames = gerar_grafico_exames_populares(exames_populares)
        grafico_termos = gerar_grafico_termos_populares(termos_populares)
        
        return render_template('admin/estatisticas.html',
                             total_exames=total_exames,
                             total_unidades=total_unidades,
                             total_avisos=total_avisos,
                             acessos_hoje=acessos_hoje,
                             acessos_semana=acessos_semana,
                             exames_populares=exames_populares,
                             termos_populares=termos_populares,
                             grafico_exames=grafico_exames,
                             grafico_termos=grafico_termos)
    
    @app.route('/admin/relatorios/logs')
    @login_required
    def logs_acesso():
        """Logs de acesso ao sistema"""
        page = request.args.get('page', 1, type=int)
        per_page = 50
        
        # Filtros
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        ip = request.args.get('ip')
        pagina = request.args.get('pagina')
        
        query = LogAcesso.query
        
        if data_inicio:
            try:
                data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
                query = query.filter(LogAcesso.created_at >= data_inicio)
            except ValueError:
                pass
        
        if data_fim:
            try:
                data_fim = datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1)
                query = query.filter(LogAcesso.created_at < data_fim)
            except ValueError:
                pass
        
        if ip:
            query = query.filter(LogAcesso.ip_address.like(f'%{ip}%'))
        
        if pagina:
            query = query.filter(LogAcesso.pagina.like(f'%{pagina}%'))
        
        logs = query.order_by(LogAcesso.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('admin/logs.html', logs=logs)
    
    @app.route('/admin/relatorios/exportar')
    @login_required
    def exportar_relatorio():
        """Exportar relatórios em Excel"""
        tipo = request.args.get('tipo', 'estatisticas')
        formato = request.args.get('formato', 'excel')
        
        if tipo == 'estatisticas':
            return exportar_estatisticas(formato)
        elif tipo == 'logs':
            return exportar_logs(formato)
        elif tipo == 'exames':
            return exportar_exames(formato)
        else:
            flash('Tipo de relatório inválido', 'error')
            return redirect(url_for('relatorios'))
    
    def gerar_grafico_exames_populares(exames_populares):
        """Gera gráfico de exames mais populares"""
        if not MATPLOTLIB_AVAILABLE or plt is None:
            return None
            
        if not exames_populares:
            return None
        
        # Configurar estilo
        plt.style.use('default')
        if sns is not None:
            sns.set_palette("husl")
        
        # Preparar dados
        nomes = [exame[0] for exame in exames_populares]
        consultas = [exame[1] for exame in exames_populares]
        
        # Criar gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(nomes, consultas, color='skyblue', alpha=0.7)
        
        # Configurar gráfico
        ax.set_xlabel('Número de Consultas')
        ax.set_title('Exames Mais Consultados (Últimos 30 dias)')
        ax.invert_yaxis()
        
        # Adicionar valores nas barras
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                   f'{int(width)}', ha='left', va='center')
        
        plt.tight_layout()
        
        # Converter para base64
        img = BytesIO()
        plt.savefig(img, format='png', dpi=300, bbox_inches='tight')
        img.seek(0)
        plt.close()
        
        return base64.b64encode(img.getvalue()).decode()
    
    def gerar_grafico_termos_populares(termos_populares):
        """Gera gráfico de termos de busca mais populares"""
        if not MATPLOTLIB_AVAILABLE or plt is None:
            return None
            
        if not termos_populares:
            return None
        
        # Configurar estilo
        plt.style.use('default')
        if sns is not None:
            sns.set_palette("Set2")
        
        # Preparar dados
        termos = [termo[0] for termo in termos_populares]
        buscas = [termo[1] for termo in termos_populares]
        
        # Criar gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(termos, buscas, color='lightcoral', alpha=0.7)
        
        # Configurar gráfico
        ax.set_xlabel('Número de Buscas')
        ax.set_title('Termos de Busca Mais Populares (Últimos 30 dias)')
        ax.invert_yaxis()
        
        # Adicionar valores nas barras
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                   f'{int(width)}', ha='left', va='center')
        
        plt.tight_layout()
        
        # Converter para base64
        img = BytesIO()
        plt.savefig(img, format='png', dpi=300, bbox_inches='tight')
        img.seek(0)
        plt.close()
        
        return base64.b64encode(img.getvalue()).decode()
    
    def exportar_estatisticas(formato):
        """Exporta estatísticas em Excel"""
        # Dados dos últimos 30 dias
        inicio = datetime.utcnow() - timedelta(days=30)
        
        # Estatísticas de exames
        exames_stats = db.session.query(
            Exame.nome,
            func.count(EstatisticaExame.id).label('visualizacoes'),
            func.count(EstatisticaExame.query.filter(
                EstatisticaExame.tipo_consulta == 'busca'
            ).subquery()).label('buscas')
        ).outerjoin(EstatisticaExame).filter(
            EstatisticaExame.created_at >= inicio
        ).group_by(Exame.id, Exame.nome).all()
        
        # Estatísticas de busca
        termos_stats = db.session.query(
            EstatisticaBusca.termo_busca,
            func.count(EstatisticaBusca.id).label('total_buscas'),
            func.avg(EstatisticaBusca.resultados_encontrados).label('media_resultados')
        ).filter(
            EstatisticaBusca.created_at >= inicio
        ).group_by(EstatisticaBusca.termo_busca).all()
        
        # Criar DataFrame
        df_exames = pd.DataFrame(exames_stats, columns=['Exame', 'Visualizações', 'Buscas'])
        df_termos = pd.DataFrame(termos_stats, columns=['Termo de Busca', 'Total de Buscas', 'Média de Resultados'])
        
        # Exportar
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_exames.to_excel(writer, sheet_name='Estatísticas de Exames', index=False)
            df_termos.to_excel(writer, sheet_name='Termos de Busca', index=False)
        
        output.seek(0)
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'estatisticas_{datetime.now().strftime("%Y%m%d")}.xlsx'
        )
    
    def exportar_logs(formato):
        """Exporta logs de acesso em Excel"""
        # Filtros
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        
        query = LogAcesso.query
        
        if data_inicio:
            try:
                data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
                query = query.filter(LogAcesso.created_at >= data_inicio)
            except ValueError:
                pass
        
        if data_fim:
            try:
                data_fim = datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1)
                query = query.filter(LogAcesso.created_at < data_fim)
            except ValueError:
                pass
        
        logs = query.order_by(LogAcesso.created_at.desc()).limit(10000).all()
        
        # Criar DataFrame
        data = []
        for log in logs:
            data.append({
                'Data/Hora': log.created_at,
                'IP': log.ip_address,
                'Página': log.pagina,
                'Método': log.metodo,
                'Status': log.status_code,
                'Tempo Resposta (s)': log.tempo_resposta,
                'User Agent': log.user_agent,
                'Referrer': log.referrer
            })
        
        df = pd.DataFrame(data)
        
        # Exportar
        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'logs_acesso_{datetime.now().strftime("%Y%m%d")}.xlsx'
        )
    
    def exportar_exames(formato):
        """Exporta lista de exames em Excel"""
        exames = Exame.query.all()
        
        # Criar DataFrame
        data = []
        for exame in exames:
            data.append({
                'Nome': exame.nome,
                'Descrição': exame.descricao,
                'Preparo': exame.preparo,
                'Documentos': exame.documentos,
                'Pós-Exame': exame.pos_exame,
                'Tempo': exame.tempo,
                'Data Criação': exame.created_at,
                'Última Atualização': exame.updated_at
            })
        
        df = pd.DataFrame(data)
        
        # Exportar
        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'exames_{datetime.now().strftime("%Y%m%d")}.xlsx'
        )

    @app.route('/admin/configuracoes', methods=['GET', 'POST'])
    @login_required
    def admin_configuracoes():
        """Gerenciar configurações gerais do site"""
        # Buscar ou criar configurações
        config = SiteConfig.query.first()
        if not config:
            config = SiteConfig()
            db.session.add(config)
            db.session.commit()
        
        form = SiteConfigForm()
        
        if form.validate_on_submit():
            # Atualizar configurações básicas
            config.nome_site = form.nome_site.data
            config.descricao_site = form.descricao_site.data
            config.email_contato = form.email_contato.data
            config.telefone_principal = form.telefone_principal.data
            config.whatsapp = form.whatsapp.data
            
            # Atualizar configurações do mapa
            config.google_maps_api_key = form.google_maps_api_key.data
            config.google_maps_embed_url = form.google_maps_embed_url.data
            
            # Atualizar SEO
            config.meta_keywords = form.meta_keywords.data
            config.meta_description = form.meta_description.data
            
            # Atualizar tema
            config.cor_primaria = form.cor_primaria.data
            config.cor_secundaria = form.cor_secundaria.data
            
            # Atualizar configurações de exibição
            config.mostrar_contatos = form.mostrar_contatos.data
            config.mostrar_mapa = form.mostrar_mapa.data
            config.mostrar_redes_sociais = form.mostrar_redes_sociais.data
            
            db.session.commit()
            flash('Configurações atualizadas com sucesso!', 'success')
            return redirect(url_for('admin_configuracoes'))
        
        elif request.method == 'GET':
            # Preencher formulário com dados existentes
            form.nome_site.data = config.nome_site
            form.descricao_site.data = config.descricao_site
            form.email_contato.data = config.email_contato
            form.telefone_principal.data = config.telefone_principal
            form.whatsapp.data = config.whatsapp
            form.google_maps_api_key.data = config.google_maps_api_key
            form.google_maps_embed_url.data = config.google_maps_embed_url
            form.meta_keywords.data = config.meta_keywords
            form.meta_description.data = config.meta_description
            form.cor_primaria.data = config.cor_primaria
            form.cor_secundaria.data = config.cor_secundaria
            form.mostrar_contatos.data = config.mostrar_contatos
            form.mostrar_mapa.data = config.mostrar_mapa
            form.mostrar_redes_sociais.data = config.mostrar_redes_sociais
        
        return render_template('admin/configuracoes.html', form=form, config=config)

    @app.route('/admin/configuracoes/enderecos', methods=['GET', 'POST'])
    @login_required
    def admin_configuracoes_enderecos():
        """Gerenciar endereços do site"""
        config = SiteConfig.query.first()
        if not config:
            config = SiteConfig()
            db.session.add(config)
            db.session.commit()
        
        if request.method == 'POST':
            action = request.form.get('action')
            
            if action == 'adicionar':
                novo_endereco = {
                    'id': len(config.get_enderecos()) + 1,
                    'nome': request.form.get('nome'),
                    'endereco': request.form.get('endereco'),
                    'bairro': request.form.get('bairro'),
                    'cidade': request.form.get('cidade'),
                    'estado': request.form.get('estado'),
                    'cep': request.form.get('cep'),
                    'telefones': request.form.get('telefones', '').split(','),
                    'horarios': request.form.get('horarios'),
                    'coordenadas': request.form.get('coordenadas')
                }
                
                enderecos = config.get_enderecos()
                enderecos.append(novo_endereco)
                config.set_enderecos(enderecos)
                
            elif action == 'editar':
                endereco_id = int(request.form.get('endereco_id'))
                enderecos = config.get_enderecos()
                
                for endereco in enderecos:
                    if endereco['id'] == endereco_id:
                        endereco.update({
                            'nome': request.form.get('nome'),
                            'endereco': request.form.get('endereco'),
                            'bairro': request.form.get('bairro'),
                            'cidade': request.form.get('cidade'),
                            'estado': request.form.get('estado'),
                            'cep': request.form.get('cep'),
                            'telefones': request.form.get('telefones', '').split(','),
                            'horarios': request.form.get('horarios'),
                            'coordenadas': request.form.get('coordenadas')
                        })
                        break
                
                config.set_enderecos(enderecos)
                
            elif action == 'excluir':
                endereco_id = int(request.form.get('endereco_id'))
                enderecos = config.get_enderecos()
                enderecos = [e for e in enderecos if e['id'] != endereco_id]
                config.set_enderecos(enderecos)
            
            db.session.commit()
            flash('Endereços atualizados com sucesso!', 'success')
            return redirect(url_for('admin_configuracoes_enderecos'))
        
        return render_template('admin/configuracoes_enderecos.html', config=config)

    @app.route('/admin/configuracoes/redes-sociais', methods=['GET', 'POST'])
    @login_required
    def admin_configuracoes_redes_sociais():
        """Gerenciar redes sociais do site"""
        config = SiteConfig.query.first()
        if not config:
            config = SiteConfig()
            db.session.add(config)
            db.session.commit()
        
        if request.method == 'POST':
            action = request.form.get('action')
            
            if action == 'adicionar':
                nova_rede = {
                    'id': len(config.get_redes_sociais()) + 1,
                    'nome': request.form.get('nome'),
                    'url': request.form.get('url'),
                    'icone': request.form.get('icone'),
                    'ativo': True
                }
                
                redes = config.get_redes_sociais()
                redes.append(nova_rede)
                config.set_redes_sociais(redes)
                
            elif action == 'editar':
                rede_id = int(request.form.get('rede_id'))
                redes = config.get_redes_sociais()
                
                for rede in redes:
                    if rede['id'] == rede_id:
                        rede.update({
                            'nome': request.form.get('nome'),
                            'url': request.form.get('url'),
                            'icone': request.form.get('icone'),
                            'ativo': request.form.get('ativo') == 'on'
                        })
                        break
                
                config.set_redes_sociais(redes)
                
            elif action == 'excluir':
                rede_id = int(request.form.get('rede_id'))
                redes = config.get_redes_sociais()
                redes = [r for r in redes if r['id'] != rede_id]
                config.set_redes_sociais(redes)
            
            db.session.commit()
            flash('Redes sociais atualizadas com sucesso!', 'success')
            return redirect(url_for('admin_configuracoes_redes_sociais'))
        
        return render_template('admin/configuracoes_redes_sociais.html', config=config)

    @app.route('/admin/configuracoes/horarios', methods=['GET', 'POST'])
    @login_required
    def admin_configuracoes_horarios():
        """Gerenciar horários de funcionamento"""
        config = SiteConfig.query.first()
        if not config:
            config = SiteConfig()
            db.session.add(config)
            db.session.commit()
        
        if request.method == 'POST':
            horarios = {
                'segunda_sexta': {
                    'funcionamento': request.form.get('segunda_sexta_funcionamento'),
                    'coleta': request.form.get('segunda_sexta_coleta'),
                    'vacinacao': request.form.get('segunda_sexta_vacinacao')
                },
                'sabado': {
                    'funcionamento': request.form.get('sabado_funcionamento'),
                    'coleta': request.form.get('sabado_coleta'),
                    'vacinacao': request.form.get('sabado_vacinacao')
                },
                'domingo': {
                    'funcionamento': request.form.get('domingo_funcionamento'),
                    'coleta': request.form.get('domingo_coleta'),
                    'vacinacao': request.form.get('domingo_vacinacao')
                }
            }
            
            config.set_horarios_funcionamento(horarios)
            db.session.commit()
            flash('Horários atualizados com sucesso!', 'success')
            return redirect(url_for('admin_configuracoes_horarios'))
        
        return render_template('admin/configuracoes_horarios.html', config=config)

    @app.route('/admin/configuracoes/informacoes', methods=['GET', 'POST'])
    @login_required
    def admin_configuracoes_informacoes():
        """Gerenciar informações importantes do site"""
        config = SiteConfig.query.first()
        if not config:
            config = SiteConfig()
            db.session.add(config)
            db.session.commit()
        
        if request.method == 'POST':
            action = request.form.get('action')
            
            if action == 'adicionar':
                nova_info = {
                    'id': len(config.get_informacoes_importantes()) + 1,
                    'titulo': request.form.get('titulo'),
                    'descricao': request.form.get('descricao'),
                    'ativo': True
                }
                
                informacoes = config.get_informacoes_importantes()
                informacoes.append(nova_info)
                config.set_informacoes_importantes(informacoes)
                
            elif action == 'editar':
                info_id = int(request.form.get('info_id'))
                informacoes = config.get_informacoes_importantes()
                
                for info in informacoes:
                    if info['id'] == info_id:
                        info.update({
                            'titulo': request.form.get('titulo'),
                            'descricao': request.form.get('descricao'),
                            'ativo': request.form.get('ativo') == 'on'
                        })
                        break
                
                config.set_informacoes_importantes(informacoes)
                
            elif action == 'excluir':
                info_id = int(request.form.get('info_id'))
                informacoes = config.get_informacoes_importantes()
                informacoes = [i for i in informacoes if i['id'] != info_id]
                config.set_informacoes_importantes(informacoes)
            
            db.session.commit()
            flash('Informações atualizadas com sucesso!', 'success')
            return redirect(url_for('admin_configuracoes_informacoes'))
        
        return render_template('admin/configuracoes_informacoes.html', config=config)

    # Rotas para gerenciamento de usuários
    @app.route('/admin/usuarios')
    @login_required
    @PermissionHelper.require_permission('manage_users')
    def admin_usuarios():
        """Lista de usuários"""
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        usuarios = User.query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('admin/usuarios.html', usuarios=usuarios)

    @app.route('/admin/usuarios/add', methods=['GET', 'POST'])
    @login_required
    @PermissionHelper.require_permission('manage_users')
    def admin_add_usuario():
        """Adicionar novo usuário"""
        form = UserForm()
        
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                email=form.email.data,
                role=form.role.data,
                is_admin=form.is_admin.data,
                is_active=form.is_active.data
            )
            
            if form.password.data:
                user.set_password(form.password.data)
            
            # Definir permissões baseadas no role
            permissions = []
            if form.role.data == 'admin':
                permissions = ['edit', 'delete', 'manage_users', 'view_stats']
            elif form.role.data == 'editor':
                permissions = ['edit', 'view_stats']
            elif form.role.data == 'viewer':
                permissions = ['view_stats']
            
            user.set_permissions(permissions)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Usuário criado com sucesso!', 'success')
            return redirect(url_for('admin_usuarios'))
        
        return render_template('admin/usuario_form.html', form=form, title='Adicionar Usuário')

    @app.route('/admin/usuarios/edit/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    @PermissionHelper.require_permission('manage_users')
    def admin_edit_usuario(user_id):
        """Editar usuário"""
        user = User.query.get_or_404(user_id)
        form = UserForm(original_username=user.username, original_email=user.email)
        
        if request.method == 'GET':
            form.username.data = user.username
            form.email.data = user.email
            form.role.data = user.role
            form.is_admin.data = user.is_admin
            form.is_active.data = user.is_active
        
        if form.validate_on_submit():
            user.username = form.username.data
            user.email = form.email.data
            user.role = form.role.data
            user.is_admin = form.is_admin.data
            user.is_active = form.is_active.data
            
            if form.password.data:
                user.set_password(form.password.data)
            
            # Atualizar permissões baseadas no role
            permissions = []
            if form.role.data == 'admin':
                permissions = ['edit', 'delete', 'manage_users', 'view_stats']
            elif form.role.data == 'editor':
                permissions = ['edit', 'view_stats']
            elif form.role.data == 'viewer':
                permissions = ['view_stats']
            
            user.set_permissions(permissions)
            
            db.session.commit()
            
            flash('Usuário atualizado com sucesso!', 'success')
            return redirect(url_for('admin_usuarios'))
        
        return render_template('admin/usuario_form.html', form=form, title='Editar Usuário', user=user)

    @app.route('/admin/usuarios/delete/<int:user_id>', methods=['POST'])
    @login_required
    @PermissionHelper.require_permission('manage_users')
    def admin_delete_usuario(user_id):
        """Deletar usuário"""
        user = User.query.get_or_404(user_id)
        
        # Não permitir deletar o próprio usuário
        if user.id == current_user.id:
            flash('Você não pode deletar sua própria conta!', 'danger')
            return redirect(url_for('admin_usuarios'))
        
        # Não permitir deletar o último admin
        if user.is_admin:
            admin_count = User.query.filter_by(is_admin=True).count()
            if admin_count <= 1:
                flash('Não é possível deletar o último administrador!', 'danger')
                return redirect(url_for('admin_usuarios'))
        
        db.session.delete(user)
        db.session.commit()
        
        flash('Usuário deletado com sucesso!', 'success')
        return redirect(url_for('admin_usuarios'))

def process_excel_file(file_path):
    """Processa arquivo Excel e retorna lista de exames"""
    try:
        # Ler o arquivo Excel
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, engine='openpyxl')
        else:
            df = pd.read_excel(file_path, engine='xlrd')
        
        exames = []
        
        # Verificar se as colunas necessárias existem
        required_columns = ['nome', 'descricao', 'preparo', 'documentos', 'pos_exame', 'tempo']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return None, f"Colunas obrigatórias não encontradas: {', '.join(missing_columns)}"
        
        # Processar cada linha
        for index, row in df.iterrows():
            # Verificar se todos os campos obrigatórios estão preenchidos
            if pd.isna(row['nome']) or pd.isna(row['descricao']) or pd.isna(row['preparo']):
                continue  # Pular linhas com dados incompletos
            
            exame = {
                'nome': str(row['nome']).strip(),
                'descricao': str(row['descricao']).strip(),
                'preparo': str(row['preparo']).strip(),
                'documentos': str(row['documentos']).strip() if not pd.isna(row['documentos']) else 'RG, CPF e pedido médico',
                'pos_exame': str(row['pos_exame']).strip() if not pd.isna(row['pos_exame']) else 'Nenhuma restrição específica',
                'tempo': str(row['tempo']).strip() if not pd.isna(row['tempo']) else 'A definir',
                'categoria': str(row['categoria']).strip() if 'categoria' in df.columns and not pd.isna(row['categoria']) else 'laboratorio',
                'icone': str(row['icone']).strip() if 'icone' in df.columns and not pd.isna(row['icone']) else ''
            }
            
            exames.append(exame)
        
        return exames, None
        
    except Exception as e:
        return None, f"Erro ao processar arquivo: {str(e)}" 