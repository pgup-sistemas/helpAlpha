from flask import Flask, request, g
from config import Config
import time
import os
import markdown2
import re
from datetime import datetime
import pytz

# Importar extensões
from app.extensions import db, login_manager

# Configuração de timezone para Brasil
BRAZIL_TIMEZONE = pytz.timezone('America/Porto_Velho')

def get_brazil_time():
    """Retorna o horário atual do Brasil (Porto Velho, Rondônia)"""
    return datetime.now(BRAZIL_TIMEZONE)

def format_brazil_datetime(dt, format_str='%d/%m/%Y %H:%M'):
    """Formata datetime para formato brasileiro"""
    if dt is None:
        return ''
    
    # Se não tem timezone, assume que é UTC e converte para Brasil
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    
    # Converte para timezone do Brasil
    brazil_time = dt.astimezone(BRAZIL_TIMEZONE)
    return brazil_time.strftime(format_str)

def create_app(config_class=Config):
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configuração
    app.config.from_object(config_class)
    
    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin_login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    # Configurar segurança
    try:
        from app.security import setup_security
        setup_security(app)
        if app.debug:
<<<<<<< HEAD
            pass
    except ImportError as e:
        if app.debug:
            pass
=======
            print("✅ Módulo de segurança configurado")
    except ImportError as e:
        if app.debug:
            print(f"⚠️  Erro ao configurar segurança: {e}")
>>>>>>> 992509f6f026cc295a8e71a87170556795035cd1
    
    # Configurar rate limiting
    try:
        from app.rate_limiting import setup_rate_limiting
        setup_rate_limiting(app)
        if app.debug:
<<<<<<< HEAD
            pass
    except ImportError as e:
        if app.debug:
            pass
=======
            print("✅ Rate limiting configurado")
    except ImportError as e:
        if app.debug:
            print(f"⚠️  Erro ao configurar rate limiting: {e}")
>>>>>>> 992509f6f026cc295a8e71a87170556795035cd1
    
    # Registrar filtros Jinja2 para Markdown
    @app.template_filter('markdown')
    def markdown_filter(text):
        """Converte texto Markdown para HTML"""
        if not text:
            return ''
        
        return markdown2.markdown(text, extras=[
            'fenced-code-blocks',
            'tables',
            'break-on-newline',
            'cuddled-lists',
            'markdown-in-html'
        ])
    
    @app.template_filter('markdown_safe')
    def markdown_safe_filter(text):
        """Converte texto Markdown para HTML com segurança adicional"""
        if not text:
            return ''
        
        html = markdown2.markdown(text, extras=[
            'fenced-code-blocks',
            'tables',
            'break-on-newline',
            'cuddled-lists',
            'markdown-in-html'
        ])
        
        # Aplicar classes CSS para melhor formatação
        html = re.sub(r'<ul>', '<ul class="markdown-list">', html)
        html = re.sub(r'<ol>', '<ol class="markdown-list">', html)
        html = re.sub(r'<p>', '<p class="markdown-paragraph">', html)
        
        # Remover duplicações de classes
        html = re.sub(r'<ul class="markdown-list"><ul class="markdown-list">', '<ul class="markdown-list">', html)
        
        return html
    
    @app.template_filter('truncate_html')
    def truncate_html_filter(html_text, length=100, killwords=False, end='...'):
        """Trunca HTML de forma segura, preservando tags"""
        if not html_text:
            return ''
        
        # Se o texto já é menor que o limite, retorna como está
        if len(html_text) <= length:
            return html_text
        
        # Remover tags HTML temporariamente para contar caracteres
        import re
        text_only = re.sub(r'<[^>]+>', '', html_text)
        
        if len(text_only) <= length:
            return html_text
        
        # Truncar o texto sem tags
        if killwords:
            truncated_text = text_only[:length]
        else:
            # Encontrar o último espaço antes do limite
            truncated_text = text_only[:length].rsplit(' ', 1)[0]
        
        # Adicionar o sufixo
        truncated_text += end
        
        # Reconstruir HTML de forma simples (não perfeita, mas funcional)
        # Esta é uma implementação básica - para casos mais complexos, usar BeautifulSoup
        return truncated_text
    
    # Importar modelos para garantir que sejam registrados
    from app.models import User, Exame, Unidade, Aviso, LogAcesso, EstatisticaExame, EstatisticaBusca, SiteConfig
    
    # Registrar rotas
    from app.routes import register_routes
    from app.admin_routes import register_admin_routes
    
    register_routes(app)
    register_admin_routes(app)
    
    # Context processor para carregar configurações do site globalmente
    @app.context_processor
    def inject_site_config():
        """Injeta as configurações do site em todos os templates"""
        try:
            config = SiteConfig.query.first()
            if not config:
                # Criar configuração padrão se não existir
                config = SiteConfig()
                db.session.add(config)
                db.session.commit()
            return {'site_config': config}
        except Exception as e:
            app.logger.error(f"Erro ao carregar configurações do site: {e}")
            # Retornar configuração padrão em caso de erro
            return {'site_config': SiteConfig()}
    
<<<<<<< HEAD
    # Context processor para carregar avisos ativos globalmente
    @app.context_processor
    def inject_avisos():
        """Injeta os avisos ativos em todos os templates"""
        try:
            from app.models import Aviso
            from datetime import datetime
            import pytz
            
            agora = datetime.now(pytz.UTC)
            avisos = Aviso.query.filter(
                Aviso.is_ativo == True,
                Aviso.data_inicio <= agora,
                (Aviso.data_fim.is_(None) | (Aviso.data_fim >= agora))
            ).limit(10).all()
            
            if app.debug:
                print(f"Numero de avisos encontrados: {len(avisos)}")
                for aviso in avisos:
                    print(f"Aviso: {aviso.titulo}")
                
            return {'avisos': avisos}
        except Exception as e:
            app.logger.error(f"Erro ao carregar avisos: {e}")
            print(f"ERRO ao carregar avisos: {e}")
            return {'avisos': []}
    
=======
>>>>>>> 992509f6f026cc295a8e71a87170556795035cd1
    # Adicionar variáveis globais aos templates
    @app.context_processor
    def inject_version():
        """Injeta a versão do sistema nos templates"""
        return {
            'app_version': get_version(),
            'current_year': datetime.now().year
        }
    
    # Filtros para formatação de data/hora no Brasil
    @app.template_filter('brazil_datetime')
    def brazil_datetime_filter(dt, format_str='%d/%m/%Y %H:%M'):
        """Formata datetime para formato brasileiro"""
        return format_brazil_datetime(dt, format_str)
    
    @app.template_filter('brazil_date')
    def brazil_date_filter(dt):
        """Formata apenas a data no formato brasileiro"""
        return format_brazil_datetime(dt, '%d/%m/%Y')
    
    @app.template_filter('brazil_time')
    def brazil_time_filter(dt):
        """Formata apenas o horário no formato brasileiro"""
        return format_brazil_datetime(dt, '%H:%M')
    
    # Middleware para rastrear acessos
    @app.before_request
    def before_request():
        g.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        # Calcular tempo de resposta
        if hasattr(g, 'start_time'):
            tempo_resposta = time.time() - g.start_time
        else:
            tempo_resposta = None
        
        # Registrar log de acesso (apenas para páginas públicas)
        if not request.path.startswith('/admin') and request.method == 'GET':
            try:
                log = LogAcesso(
                    ip_address=request.remote_addr,
                    user_agent=request.headers.get('User-Agent'),
                    pagina=request.path,
                    metodo=request.method,
                    status_code=response.status_code,
                    tempo_resposta=tempo_resposta,
                    query_string=request.query_string.decode('utf-8') if request.query_string else None,
                    referrer=request.headers.get('Referer')
                )
                
                db.session.add(log)
                db.session.commit()
            except Exception as e:
                # Em caso de erro, não interromper a resposta
                app.logger.error(f"Erro ao registrar log: {e}")
        
        return response
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app

def init_database(app):
    """Inicializa o banco de dados e cria usuário admin"""
    with app.app_context():
        # Importar modelos
        from app.models import User, SiteConfig
        
        # Verificar se o banco existe
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        db_exists = os.path.exists(db_path)
        
        # Criar todas as tabelas
        db.create_all()
        
        if not db_exists:
<<<<<<< HEAD
            pass
=======
            print("🗄️  Banco de dados criado automaticamente")
>>>>>>> 992509f6f026cc295a8e71a87170556795035cd1
        
        # Criar usuário admin se não existir
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@helpalphaclinclinclin.com',
                is_admin=True,
                is_active=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
<<<<<<< HEAD
            pass
        else:
            pass
=======
            print("👤 Usuário admin criado: admin / admin123")
        else:
            print("👤 Usuário admin já existe")
>>>>>>> 992509f6f026cc295a8e71a87170556795035cd1
        
        # Criar configuração padrão do site se não existir
        site_config = SiteConfig.query.first()
        if not site_config:
            site_config = SiteConfig()
            db.session.add(site_config)
            db.session.commit()
<<<<<<< HEAD
            pass
        
        pass
=======
            print("⚙️  Configuração padrão do site criada")
        
        print("✅ Banco de dados inicializado com sucesso!")
>>>>>>> 992509f6f026cc295a8e71a87170556795035cd1

def get_version():
    """Obtém a versão do sistema do arquivo VERSION"""
    try:
        version_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'VERSION')
        if os.path.exists(version_file):
            with open(version_file, 'r') as f:
                return f.read().strip()
        return '1.0.0'  # Versão padrão
    except Exception:
<<<<<<< HEAD
        return '1.0.0'  # Versão padrão em caso de erro
=======
        return '1.0.0'  # Versão padrão em caso de erro 
>>>>>>> 992509f6f026cc295a8e71a87170556795035cd1
