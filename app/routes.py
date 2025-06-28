from flask import render_template, request, jsonify, send_file
import json
import os
from datetime import datetime

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

def register_routes(app):
    """Registra as rotas na aplicação Flask"""
    
    @app.route('/')
    def index():
        """Página inicial com busca de exames"""
        exames = load_exames()
        query = request.args.get('q', '').lower()
        
        if query:
            exames_filtrados = [e for e in exames if query in e['nome'].lower()]
        else:
            exames_filtrados = exames
        
        return render_template('index.html', exames=exames_filtrados, query=query)

    @app.route('/exame/<nome>')
    def exame(nome):
        """Página de detalhes de um exame específico"""
        exames = load_exames()
        
        # Buscar o exame pelo nome (case insensitive)
        exame = None
        for e in exames:
            if e['nome'].lower() == nome.lower():
                exame = e
                break
        
        if not exame:
            return render_template('404.html'), 404
        
        return render_template('exame.html', exame=exame)

    @app.route('/api/search')
    def api_search():
        """API para busca de exames via AJAX"""
        exames = load_exames()
        query = request.args.get('q', '').lower()
        
        if not query:
            return jsonify([])
        
        resultados = [e for e in exames if query in e['nome'].lower()]
        return jsonify(resultados[:10])  # Limitar a 10 resultados

    @app.route('/sitemap.xml')
    def sitemap():
        """Gera sitemap.xml dinamicamente"""
        exames = load_exames()
        base_url = request.url_root.rstrip('/')
        
        sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{base_url}/</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>{base_url}/admin/login</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.3</priority>
    </url>"""
        
        # Adicionar URLs dos exames
        for exame in exames:
            exame_url = f"{base_url}/exame/{exame['nome'].replace(' ', '%20')}"
            sitemap_content += f"""
    <url>
        <loc>{exame_url}</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>"""
        
        sitemap_content += """
</urlset>"""
        
        return sitemap_content, 200, {'Content-Type': 'application/xml'}

    @app.route('/robots.txt')
    def robots():
        """Gera robots.txt dinamicamente"""
        robots_content = f"""User-agent: *
Allow: /

# Sitemap
Sitemap: {request.url_root.rstrip('/')}/sitemap.xml

# Crawl-delay
Crawl-delay: 1

# Disallow admin area
Disallow: /admin/
Disallow: /admin/login
Disallow: /admin/dashboard
Disallow: /admin/exames
Disallow: /admin/upload-excel

# Allow public pages
Allow: /
Allow: /exame/
Allow: /api/search
"""
        return robots_content, 200, {'Content-Type': 'text/plain'}

    @app.errorhandler(404)
    def not_found(error):
        """Página 404 personalizada"""
        return render_template('404.html'), 404 