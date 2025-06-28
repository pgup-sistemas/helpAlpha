from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
import json
import os
import pandas as pd
from werkzeug.utils import secure_filename
from app.models import User
from app.forms import LoginForm, ExameForm, UploadExcelForm

def load_exames():
    """Carrega os dados dos exames do arquivo JSON"""
    try:
        with open('data/exames.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_exames(exames):
    """Salva os dados dos exames no arquivo JSON"""
    with open('data/exames.json', 'w', encoding='utf-8') as file:
        json.dump(exames, file, ensure_ascii=False, indent=2)

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
                'tempo': str(row['tempo']).strip() if not pd.isna(row['tempo']) else 'A definir'
            }
            
            exames.append(exame)
        
        return exames, None
        
    except Exception as e:
        return None, f"Erro ao processar arquivo: {str(e)}"

def admin_login():
    """Página de login administrativo"""
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Usuário ou senha incorretos!', 'danger')
    
    return render_template('admin/login.html', form=form)

def admin_logout():
    """Logout administrativo"""
    logout_user()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('admin_login'))

@login_required
def admin_dashboard():
    """Dashboard administrativo"""
    exames = load_exames()
    total_exames = len(exames)
    
    # Estatísticas básicas
    exames_laboratoriais = len([e for e in exames if 'laboratorial' in e['descricao'].lower() or 'sangue' in e['descricao'].lower()])
    exames_imagem = len([e for e in exames if 'imagem' in e['descricao'].lower() or 'ressonância' in e['nome'].lower() or 'tomografia' in e['nome'].lower()])
    
    return render_template('admin/dashboard.html', 
                         total_exames=total_exames,
                         exames_laboratoriais=exames_laboratoriais,
                         exames_imagem=exames_imagem)

@login_required
def admin_exames():
    """Lista de exames para administração"""
    exames = load_exames()
    return render_template('admin/exames.html', exames=exames)

@login_required
def admin_add_exame():
    """Adicionar novo exame"""
    form = ExameForm()
    
    if form.validate_on_submit():
        exames = load_exames()
        
        # Verificar se já existe um exame com o mesmo nome
        if any(e['nome'].lower() == form.nome.data.lower() for e in exames):
            flash('Já existe um exame com este nome!', 'warning')
            return render_template('admin/exame_form.html', form=form, title="Adicionar Exame")
        
        novo_exame = {
            'nome': form.nome.data,
            'descricao': form.descricao.data,
            'preparo': form.preparo.data,
            'documentos': form.documentos.data,
            'pos_exame': form.pos_exame.data,
            'tempo': form.tempo.data
        }
        
        exames.append(novo_exame)
        save_exames(exames)
        
        flash('Exame adicionado com sucesso!', 'success')
        return redirect(url_for('admin_exames'))
    
    return render_template('admin/exame_form.html', form=form, title="Adicionar Exame")

@login_required
def admin_edit_exame(nome):
    """Editar exame existente"""
    exames = load_exames()
    exame = None
    
    # Encontrar o exame pelo nome
    for e in exames:
        if e['nome'].lower() == nome.lower():
            exame = e
            break
    
    if not exame:
        flash('Exame não encontrado!', 'danger')
        return redirect(url_for('admin_exames'))
    
    form = ExameForm()
    
    if form.validate_on_submit():
        # Verificar se o novo nome já existe (exceto o próprio)
        if any(e['nome'].lower() == form.nome.data.lower() and e['nome'].lower() != nome.lower() for e in exames):
            flash('Já existe um exame com este nome!', 'warning')
            return render_template('admin/exame_form.html', form=form, title="Editar Exame")
        
        # Atualizar o exame
        exame['nome'] = form.nome.data
        exame['descricao'] = form.descricao.data
        exame['preparo'] = form.preparo.data
        exame['documentos'] = form.documentos.data
        exame['pos_exame'] = form.pos_exame.data
        exame['tempo'] = form.tempo.data
        
        save_exames(exames)
        
        flash('Exame atualizado com sucesso!', 'success')
        return redirect(url_for('admin_exames'))
    
    elif request.method == 'GET':
        # Preencher o formulário com os dados existentes
        form.nome.data = exame['nome']
        form.descricao.data = exame['descricao']
        form.preparo.data = exame['preparo']
        form.documentos.data = exame['documentos']
        form.pos_exame.data = exame['pos_exame']
        form.tempo.data = exame['tempo']
    
    return render_template('admin/exame_form.html', form=form, title="Editar Exame")

@login_required
def admin_delete_exame(nome):
    """Excluir exame"""
    exames = load_exames()
    
    # Encontrar e remover o exame
    for i, exame in enumerate(exames):
        if exame['nome'].lower() == nome.lower():
            exames.pop(i)
            save_exames(exames)
            flash('Exame excluído com sucesso!', 'success')
            break
    else:
        flash('Exame não encontrado!', 'danger')
    
    return redirect(url_for('admin_exames'))

@login_required
def admin_upload_excel():
    """Upload em massa de exames via Excel"""
    form = UploadExcelForm()
    
    if form.validate_on_submit():
        try:
            # Salvar arquivo temporariamente
            file = form.arquivo.data
            filename = secure_filename(file.filename)
            
            # Criar diretório de uploads se não existir
            upload_dir = 'uploads'
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)
            
            # Processar arquivo Excel
            exames_novos, error = process_excel_file(file_path)
            
            if error:
                flash(f'Erro no processamento: {error}', 'danger')
                # Remover arquivo temporário
                if os.path.exists(file_path):
                    os.remove(file_path)
                return render_template('admin/upload_excel.html', form=form)
            
            if not exames_novos:
                flash('Nenhum exame válido encontrado no arquivo!', 'warning')
                # Remover arquivo temporário
                if os.path.exists(file_path):
                    os.remove(file_path)
                return render_template('admin/upload_excel.html', form=form)
            
            # Carregar exames existentes
            exames_existentes = load_exames()
            
            # Verificar duplicatas
            nomes_existentes = [e['nome'].lower() for e in exames_existentes]
            exames_para_adicionar = []
            duplicatas = []
            
            for exame in exames_novos:
                if exame['nome'].lower() in nomes_existentes:
                    duplicatas.append(exame['nome'])
                else:
                    exames_para_adicionar.append(exame)
            
            # Adicionar novos exames
            exames_existentes.extend(exames_para_adicionar)
            save_exames(exames_existentes)
            
            # Remover arquivo temporário
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Mensagens de resultado
            if exames_para_adicionar:
                flash(f'{len(exames_para_adicionar)} exames importados com sucesso!', 'success')
            
            if duplicatas:
                flash(f'{len(duplicatas)} exames duplicados ignorados: {", ".join(duplicatas[:5])}{"..." if len(duplicatas) > 5 else ""}', 'warning')
            
            return redirect(url_for('admin_exames'))
            
        except Exception as e:
            flash(f'Erro durante o upload: {str(e)}', 'danger')
    
    return render_template('admin/upload_excel.html', form=form)

@login_required
def admin_download_template():
    """Download do template Excel"""
    try:
        # Criar DataFrame de exemplo
        template_data = {
            'nome': ['Hemograma Completo', 'Glicemia em Jejum', 'Colesterol Total'],
            'descricao': [
                'Avaliação das células sanguíneas para diagnóstico de anemias e infecções.',
                'Mede a quantidade de açúcar no sangue para diagnosticar diabetes.',
                'Avalia os níveis de colesterol para risco cardiovascular.'
            ],
            'preparo': [
                'Jejum de 8 horas. Evitar exercícios 24h antes.',
                'Jejum de 8-12 horas. Não ingerir água em excesso.',
                'Jejum de 12 horas. Evitar alimentos gordurosos 24h antes.'
            ],
            'documentos': [
                'RG, CPF e pedido médico original.',
                'RG, CPF, pedido médico e carteira do convênio.',
                'RG, CPF, pedido médico e carteira do convênio.'
            ],
            'pos_exame': [
                'Nenhuma restrição. Pode retomar atividades normais.',
                'Pode se alimentar normalmente após o exame.',
                'Retomar alimentação normal. Manter dieta equilibrada.'
            ],
            'tempo': ['10-15 minutos', '5-10 minutos', '10-15 minutos']
        }
        
        df = pd.DataFrame(template_data)
        
        # Criar diretório de downloads se não existir
        download_dir = 'downloads'
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        template_path = os.path.join(download_dir, 'template_exames.xlsx')
        df.to_excel(template_path, index=False, engine='openpyxl')
        
        from flask import send_file
        return send_file(template_path, as_attachment=True, download_name='template_exames.xlsx')
        
    except Exception as e:
        flash(f'Erro ao gerar template: {str(e)}', 'danger')
        return redirect(url_for('admin_upload_excel')) 