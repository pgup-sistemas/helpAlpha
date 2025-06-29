"""
Módulo de Rate Limiting para Help Alphaclin
Implementa proteção contra ataques de força bruta e spam
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request, g, current_app
from app.security import RateLimitHelper

# Instância global do limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
    strategy="fixed-window"
)

def setup_rate_limiting(app):
    """Configura o rate limiting na aplicação"""
    
    # Inicializar o limiter
    limiter.init_app(app)
    
    # Configurar error handler para rate limiting
    @app.errorhandler(429)
    def ratelimit_handler(e):
        """Handler personalizado para rate limiting"""
        return {
            'error': 'Limite de requisições excedido',
            'message': 'Você fez muitas requisições. Tente novamente mais tarde.',
            'retry_after': getattr(e, 'retry_after', 60)
        }, 429, {
            'Retry-After': getattr(e, 'retry_after', 60),
            'X-RateLimit-Limit': getattr(e, 'limit', 'unknown'),
            'X-RateLimit-Remaining': getattr(e, 'remaining', 'unknown'),
            'X-RateLimit-Reset': getattr(e, 'reset', 'unknown')
        }

def get_rate_limit_key():
    """Obtém chave personalizada para rate limiting"""
    # Se o usuário está logado, usar ID do usuário
    if hasattr(g, 'user') and g.user and hasattr(g.user, 'id'):
        return f"user:{g.user.id}"
    
    # Caso contrário, usar IP
    return f"ip:{RateLimitHelper.get_client_ip()}"

# Decoradores para aplicar rate limiting
def login_rate_limit(f):
    """Decorador para rate limiting de login"""
    return limiter.limit("5 per minute")(limiter.limit("20 per hour")(f))

def upload_rate_limit(f):
    """Decorador para rate limiting de upload"""
    return limiter.limit("10 per hour")(limiter.limit("50 per day")(f))

def search_rate_limit(f):
    """Decorador para rate limiting de busca"""
    return limiter.limit("100 per minute")(limiter.limit("1000 per hour")(f))

def api_rate_limit(f):
    """Decorador para rate limiting de API"""
    return limiter.limit("200 per minute")(limiter.limit("2000 per hour")(f))

def admin_rate_limit(f):
    """Decorador para rate limiting de admin"""
    return limiter.limit("30 per hour")(limiter.limit("100 per day")(f))

def reset_password_rate_limit(f):
    """Decorador para rate limiting de redefinição de senha"""
    return limiter.limit("3 per hour")(limiter.limit("10 per day")(f))

# Funções auxiliares para configuração dinâmica
def configure_dynamic_limits(app):
    """Configura limites dinâmicos baseados no ambiente"""
    
    if app.config.get('FLASK_ENV') == 'production':
        # Limites mais restritivos em produção
        limiter.limit("100 per day")(app.view_functions.get('index'))
        limiter.limit("50 per hour")(app.view_functions.get('buscar'))
    else:
        # Limites mais permissivos em desenvolvimento
        limiter.limit("1000 per day")(app.view_functions.get('index'))
        limiter.limit("500 per hour")(app.view_functions.get('buscar'))

def get_rate_limit_info():
    """Obtém informações sobre rate limiting para debug"""
    return {
        'current_ip': RateLimitHelper.get_client_ip(),
        'user_identifier': get_rate_limit_key(),
        'limits': {
            'default': "200 per day, 50 per hour",
            'login': "5 per minute, 20 per hour",
            'upload': "10 per hour, 50 per day",
            'search': "100 per minute, 1000 per hour",
            'api': "200 per minute, 2000 per hour",
            'admin': "30 per hour, 100 per day",
            'reset_password': "3 per hour, 10 per day"
        }
    } 