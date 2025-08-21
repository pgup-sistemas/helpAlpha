"""
Módulo de segurança para Help Alphaclin
Implementa headers de segurança e outras proteções
"""

from flask import request, g, flash, redirect, url_for
from flask_login import current_user
import re
from functools import wraps

class SecurityMiddleware:
    """Middleware para adicionar headers de segurança"""
    
    def __init__(self, app):
        self.app = app
        self.setup_security_headers()
    
    def setup_security_headers(self):
        """Configura os headers de segurança"""
        
        @self.app.after_request
        def add_security_headers(response):
            """Adiciona headers de segurança à resposta"""
            
            # Headers básicos de segurança
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'SAMEORIGIN'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            
            # Content Security Policy
            csp_policy = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' cdnjs.cloudflare.com *.googleapis.com *.google.com; "
                "style-src 'self' 'unsafe-inline' cdnjs.cloudflare.com fonts.googleapis.com *.googleapis.com; "
                "font-src 'self' cdnjs.cloudflare.com fonts.gstatic.com *.googleapis.com; "
                "img-src 'self' data: *.googleapis.com *.google.com *.gstatic.com; "
                "connect-src 'self' *.googleapis.com *.google.com; "
                "frame-src 'self' *.google.com *.googleapis.com; "
                "frame-ancestors 'self'; "
                "base-uri 'self'; "
                "form-action 'self'"
            )
            response.headers['Content-Security-Policy'] = csp_policy
            
            # HSTS (HTTP Strict Transport Security) - apenas para HTTPS
            if request.is_secure:
                response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
            
            # Permissions Policy (anteriormente Feature Policy)
            permissions_policy = (
                "geolocation=(), "
                "microphone=(), "
                "camera=(), "
                "payment=(), "
                "usb=(), "
                "magnetometer=(), "
                "gyroscope=(), "
                "accelerometer=()"
            )
            response.headers['Permissions-Policy'] = permissions_policy
            
            return response
    
    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

class InputSanitizer:
    """Classe para sanitização de entrada"""
    
    @staticmethod
    def sanitize_string(value):
        """Sanitiza uma string removendo caracteres perigosos"""
        if not value:
            return value
        
        # Remover caracteres de controle
        value = re.sub(r'[\x00-\x1f\x7f]', '', str(value))
        
        # Remover scripts básicos
        value = re.sub(r'<script[^>]*>.*?</script>', '', value, flags=re.IGNORECASE | re.DOTALL)
        value = re.sub(r'javascript:', '', value, flags=re.IGNORECASE)
        value = re.sub(r'on\w+\s*=', '', value, flags=re.IGNORECASE)
        
        return value.strip()
    
    @staticmethod
    def sanitize_filename(filename):
        """Sanitiza nome de arquivo"""
        if not filename:
            return filename
        
        # Remover caracteres perigosos
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'\.\.', '', filename)  # Prevenir directory traversal
        
        return filename
    
    @staticmethod
    def validate_email(email):
        """Valida formato de email"""
        if not email:
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

class RateLimitHelper:
    """Helper para configurações de rate limiting"""
    
    @staticmethod
    def get_client_ip():
        """Obtém o IP real do cliente"""
        # Verificar headers de proxy
        forwarded_for = request.headers.get('X-Forwarded-For')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()
        elif request.headers.get('X-Real-IP'):
            return request.headers.get('X-Real-IP')
        else:
            return request.remote_addr
    
    @staticmethod
    def get_user_identifier():
        """Obtém identificador único do usuário para rate limiting"""
        # Se o usuário está logado, usar o ID
        if hasattr(g, 'user') and g.user and hasattr(g.user, 'id'):
            return f"user:{g.user.id}"
        
        # Caso contrário, usar IP
        return f"ip:{RateLimitHelper.get_client_ip()}"

def setup_security(app):
    """Configura todas as medidas de segurança"""
    
    # Adicionar middleware de segurança
    SecurityMiddleware(app)
    
    # Configurar sanitização global (apenas para logs e validação)
    @app.before_request
    def sanitize_inputs():
        """Sanitiza entradas antes do processamento"""
        sanitizer = InputSanitizer()
        
        # Sanitizar parâmetros GET (apenas para logs)
        sanitized_args = {}
        for key, value in request.args.items():
            sanitized_args[key] = sanitizer.sanitize_string(value)
        
        # Sanitizar parâmetros POST (apenas para logs)
        sanitized_form = {}
        if request.form:
            for key, value in request.form.items():
                sanitized_form[key] = sanitizer.sanitize_string(value)
        
        # Armazenar dados sanitizados em g para uso posterior
        g.sanitized_args = sanitized_args
        g.sanitized_form = sanitized_form
        
        # Sanitizar JSON (apenas para logs)
        if request.is_json:
            try:
                json_data = request.get_json()
                if json_data:
                    sanitized_json = sanitize_json(json_data, sanitizer)
                    g.sanitized_json = sanitized_json
            except Exception:
                pass
    
    @app.errorhandler(413)
    def too_large(error):
        """Handler para arquivos muito grandes"""
        return {'error': 'Arquivo muito grande'}, 413
    
    @app.errorhandler(429)
    def too_many_requests(error):
        """Handler para rate limiting"""
        return {'error': 'Muitas requisições. Tente novamente mais tarde.'}, 429

def sanitize_json(data, sanitizer):
    """Sanitiza dados JSON recursivamente"""
    if isinstance(data, dict):
        return {key: sanitize_json(value, sanitizer) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_json(item, sanitizer) for item in data]
    elif isinstance(data, str):
        return sanitizer.sanitize_string(data)
    else:
        return data

class PermissionHelper:
    """Helper para verificação de permissões"""
    
    @staticmethod
    def require_permission(permission):
        """Decorador para verificar permissão específica"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not current_user.is_authenticated:
                    return redirect(url_for('admin_login'))
                
                if current_user.has_permission(permission):
                    return f(*args, **kwargs)
                
                flash('Acesso negado! Você não tem permissão para esta ação.', 'danger')
                return redirect(url_for('admin_dashboard'))
            return decorated_function
        return decorator
    
    @staticmethod
    def require_role(role):
        """Decorador para verificar role específica"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not current_user.is_authenticated:
                    return redirect(url_for('admin_login'))
                
                if current_user.is_admin or current_user.role == role:
                    return f(*args, **kwargs)
                
                flash('Acesso negado! Você não tem o nível de acesso necessário.', 'danger')
                return redirect(url_for('admin_dashboard'))
            return decorated_function
        return decorator
    
    @staticmethod
    def require_edit_permission(f):
        """Decorador para verificar permissão de edição"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('admin_login'))
            
            if current_user.can_edit():
                return f(*args, **kwargs)
            
            flash('Acesso negado! Você não pode editar conteúdo.', 'danger')
            return redirect(url_for('admin_dashboard'))
        return decorated_function
    
    @staticmethod
    def require_admin_or_edit(f):
        """Decorador para verificar se é admin ou pode editar"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('admin_login'))
            
            if current_user.is_admin or current_user.can_edit():
                return f(*args, **kwargs)
            
            flash('Acesso negado! Apenas administradores e editores podem realizar esta ação.', 'danger')
            return redirect(url_for('admin_dashboard'))
        return decorated_function 