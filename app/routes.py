from flask import render_template, request, jsonify, send_file, current_app, redirect, url_for, send_from_directory, flash
import json
import os
from datetime import datetime
import math
from app.models import Exame, Aviso, EstatisticaExame, EstatisticaBusca, Unidade, SiteConfig
from app.extensions import db
from sqlalchemy import or_

# Importar decoradores de rate limiting
try:
    from app.rate_limiting import search_rate_limit, api_rate_limit
except ImportError:
    # Fallback se o rate limiting não estiver disponível
    def search_rate_limit(f): return f
    def api_rate_limit(f): return f

def load_exames():
    """Carrega os dados dos exames do arquivo JSON"""
    try:
        with open('data/exames.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def search_exames(query):
    """Busca exames por nome"""
    exames = load_exames()
    query = query.lower()
    return [e for e in exames if query in e['nome'].lower()]

def get_exame_by_name(nome):
    """Busca um exame específico pelo nome"""
    exames = load_exames()
    for exame in exames:
        if exame['nome'].lower() == nome.lower():
            return exame
    return None

def get_avisos_ativos():
    """Busca avisos ativos e válidos"""
    agora = datetime.utcnow()
    
    avisos = Aviso.query.filter(
        Aviso.is_ativo == True,
        Aviso.data_inicio <= agora,
        (Aviso.data_fim.is_(None) | (Aviso.data_fim >= agora))
    ).order_by(Aviso.data_inicio.desc()).limit(5).all()
    
    return avisos

def paginate_exames(exames, page=1, per_page=9):
    """Pagina a lista de exames"""
    total = len(exames)
    total_pages = math.ceil(total / per_page)
    
    # Validar página
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages
    
    # Calcular índices
    start = (page - 1) * per_page
    end = start + per_page
    
    # Criar objeto de paginação compatível com o template
    class Pagination:
        def __init__(self, items, page, per_page, total, total_pages):
            self.items = items
            self.page = page
            self.per_page = per_page
            self.total = total
            self.total_pages = total_pages
            self.pages = total_pages  # Alias para compatibilidade
            self.has_prev = page > 1
            self.has_next = page < total_pages
            self.prev_page = page - 1 if page > 1 else None
            self.next_page = page + 1 if page < total_pages else None
        
        def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
            """Gera números de página para exibição"""
            last = 0
            for num in range(1, self.total_pages + 1):
                if (num <= left_edge or 
                    (num > self.page - left_current - 1 and 
                     num < self.page + right_current) or 
                    num > self.total_pages - right_edge):
                    if last + 1 != num:
                        yield None
                    yield num
                    last = num
    
    return Pagination(
        items=exames[start:end],
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages
    )

def register_routes(app):
    """Registra as rotas da aplicação"""

    @app.route('/admin/avisos/ativar/<int:aviso_id>', methods=['POST'])
    def admin_ativar_aviso(aviso_id):
        aviso = Aviso.query.get_or_404(aviso_id)
        aviso.is_ativo = True
        db.session.commit()
        flash('Aviso ativado com sucesso!', 'success')
        return redirect(url_for('admin_avisos'))

    @app.route('/admin/avisos/desativar/<int:aviso_id>', methods=['POST'])
    def admin_desativar_aviso(aviso_id):
        aviso = Aviso.query.get_or_404(aviso_id)
        aviso.is_ativo = False
        db.session.commit()
        flash('Aviso desativado com sucesso!', 'warning')
        return redirect(url_for('admin_avisos'))

    # ====== NOVA ROTA: Configurações do Site com upload de logo ======
    from flask_login import login_required, current_user
    from werkzeug.utils import secure_filename
    from app.forms import SiteConfigForm



    """Registra as rotas da aplicação"""
    
    @app.route('/')
    def index():
        """Página inicial"""
        # Buscar configurações do site
        config = SiteConfig.query.first()
        if not config:
            config = SiteConfig()
        
        # Buscar todos os exames
        exames = Exame.query
        
        # Filtro por categoria
        categoria = request.args.get('categoria')
        if categoria:
            exames = exames.filter_by(categoria=categoria)
        
        exames = exames.all()
        
        # Paginação
        page = request.args.get('page', 1, type=int)
        pagination = paginate_exames(exames, page=page, per_page=9)
        
        # Query de busca (se houver)
        query = request.args.get('q', '')
        
        # Buscar unidades ativas
        unidades = Unidade.query.filter_by(is_ativo=True).all()
        
        # Buscar avisos ativos
        agora = datetime.utcnow()
        avisos = Aviso.query.filter(
            Aviso.is_ativo == True,
            Aviso.data_inicio <= agora,
            (Aviso.data_fim.is_(None) | (Aviso.data_fim >= agora))
        ).limit(3).all()
        
        return render_template('index.html', 
                             exames=pagination.items, 
                             pagination=pagination,
                             query=query,
                             unidades=unidades, 
                             avisos=avisos,
                             config=config)
    
    @app.route('/buscar')
    @search_rate_limit
    def buscar():
        """Busca de exames"""
        query = request.args.get('q', '').strip()
        
        if not query:
            # Se não há query, redirecionar para a página inicial
            return redirect(url_for('index'))
        
        # Buscar exames que contenham o termo na busca
        exames = Exame.query.filter(
            or_(
                Exame.nome.ilike(f'%{query}%'),
                Exame.descricao.ilike(f'%{query}%')
            )
        )
        
        # Filtro por categoria
        categoria = request.args.get('categoria')
        if categoria:
            exames = exames.filter_by(categoria=categoria)
        
        exames = exames.all()
        
        # Paginação
        page = request.args.get('page', 1, type=int)
        pagination = paginate_exames(exames, page=page, per_page=9)
        
        # Buscar avisos ativos
        agora = datetime.utcnow()
        avisos = Aviso.query.filter(
            Aviso.is_ativo == True,
            Aviso.data_inicio <= agora,
            (Aviso.data_fim.is_(None) | (Aviso.data_fim >= agora))
        ).all()
        
        # Registrar estatística de busca
        try:
            estatistica = EstatisticaBusca(
                termo_busca=query,
                resultados_encontrados=len(exames),
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent')
            )
            db.session.add(estatistica)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(f"Erro ao registrar estatística de busca: {e}")
        
        return render_template('index.html', 
                             exames=pagination.items, 
                             pagination=pagination,
                             query=query,
                             avisos=avisos)
    
    @app.route('/exame/<nome_exame>')
    def exame(nome_exame):
        """Página de detalhes do exame"""
        exame = Exame.query.filter_by(nome=nome_exame).first_or_404()
        
        # Registrar estatística de visualização
        try:
            estatistica = EstatisticaExame(
                exame_id=exame.id,
                tipo_consulta='visualizacao',
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent')
            )
            db.session.add(estatistica)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(f"Erro ao registrar estatística de visualização: {e}")
        
        return render_template('exame.html', exame=exame)
    
    @app.route('/api/buscar')
    @api_rate_limit
    def api_buscar():
        """API para busca de exames (AJAX)"""
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify([])
        
        # Buscar exames
        exames = Exame.query.filter(
            or_(
                Exame.nome.ilike(f'%{query}%'),
                Exame.descricao.ilike(f'%{query}%')
            )
        ).limit(10).all()
        
        # Registrar estatística de busca
        try:
            estatistica = EstatisticaBusca(
                termo_busca=query,
                resultados_encontrados=len(exames),
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent')
            )
            db.session.add(estatistica)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(f"Erro ao registrar estatística de busca API: {e}")
        
        # Retornar resultados em JSON
        resultados = []
        for exame in exames:
            resultados.append({
                'id': exame.id,
                'nome': exame.nome,
                'categoria': exame.categoria_display,
                'url': url_for('exame', nome_exame=exame.nome)
            })
        
        return jsonify(resultados)

    @app.route('/sitemap.xml')
    def sitemap():
        """Gera o sitemap.xml dinamicamente"""
        # URLs estáticas principais
        urls = [
            {
                'loc': request.url_root.rstrip('/'),
                'lastmod': datetime.utcnow().strftime('%Y-%m-%d'),
                'changefreq': 'daily',
                'priority': '1.0'
            }
        ]
        
        # URLs dos exames
        exames = Exame.query.all()
        for exame in exames:
            urls.append({
                'loc': f"{request.url_root.rstrip('/')}/exame/{exame.nome}",
                'lastmod': exame.updated_at.strftime('%Y-%m-%d') if exame.updated_at else datetime.utcnow().strftime('%Y-%m-%d'),
                'changefreq': 'weekly',
                'priority': '0.8'
            })
        
        # URLs das unidades
        unidades = Unidade.query.filter_by(is_ativo=True).all()
        for unidade in unidades:
            urls.append({
                'loc': f"{request.url_root.rstrip('/')}/unidade/{unidade.id}",
                'lastmod': unidade.updated_at.strftime('%Y-%m-%d') if unidade.updated_at else datetime.utcnow().strftime('%Y-%m-%d'),
                'changefreq': 'monthly',
                'priority': '0.6'
            })
        
        # Gerar XML do sitemap
        sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""
        
        for url in urls:
            sitemap_xml += f"""  <url>
    <loc>{url['loc']}</loc>
    <lastmod>{url['lastmod']}</lastmod>
    <changefreq>{url['changefreq']}</changefreq>
    <priority>{url['priority']}</priority>
  </url>
"""
        
        sitemap_xml += "</urlset>"
        
        response = app.response_class(sitemap_xml, mimetype='application/xml')
        return response

    @app.route('/robots.txt')
    def robots():
        """Gera o robots.txt dinamicamente"""
        robots_content = f"""User-agent: *
Allow: /

# Sitemap
Sitemap: {request.url_root.rstrip('/')}/sitemap.xml

# Crawl-delay (opcional - 1 segundo entre requisições)
Crawl-delay: 1

# Bloquear acesso a áreas administrativas
Disallow: /admin/
Disallow: /admin/login
Disallow: /admin/logout
Disallow: /admin/reset-password

# Bloquear acesso a arquivos sensíveis
Disallow: /config.py
Disallow: /requirements.txt
Disallow: /run.py
Disallow: /migrate_*.py
Disallow: /*.db
Disallow: /instance/
Disallow: /venv/
Disallow: /.env
Disallow: /.git/

# Permitir acesso a arquivos estáticos
Allow: /static/
Allow: /static/css/
Allow: /static/images/
Allow: /static/js/

# Informações sobre o site
# Help Alphaclin - Exames e Vacinas
# Porto Velho, Rondônia
# Desenvolvido por PageUp Sistemas
"""
        
        response = app.response_class(robots_content, mimetype='text/plain')
        return response

    @app.errorhandler(404)
    def not_found(error):
        """Handler para página não encontrada"""
        return render_template('404.html'), 404 