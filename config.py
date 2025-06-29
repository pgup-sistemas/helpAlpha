import os
from datetime import timedelta, datetime
from dotenv import load_dotenv
import pytz

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração de timezone para Brasil (Porto Velho, Rondônia)
TIMEZONE = pytz.timezone('America/Porto_Velho')

def get_brazil_time():
    """Retorna o horário atual do Brasil"""
    return datetime.now(TIMEZONE)

class Config:
    """Configurações base da aplicação"""
    # Chave secreta - CRÍTICO: Alterar em produção!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configurações do banco de dados
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///helpalphaclinclinclinclin.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de segurança
    WTF_CSRF_ENABLED = os.environ.get('WTF_CSRF_ENABLED', 'True').lower() == 'true'
    WTF_CSRF_TIME_LIMIT = int(os.environ.get('WTF_CSRF_TIME_LIMIT', 3600))  # 1 hora
    
    # Configurações de sessão
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=int(os.environ.get('PERMANENT_SESSION_LIFETIME', 28800)))  # 8 horas
    
    # Configurações de upload
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB max file size
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'app/uploads')
    DOWNLOAD_FOLDER = os.environ.get('DOWNLOAD_FOLDER', 'app/downloads')
    
    # Configurações de paginação
    EXAMES_PER_PAGE = int(os.environ.get('EXAMES_PER_PAGE', 9))
    ADMIN_EXAMES_PER_PAGE = int(os.environ.get('ADMIN_EXAMES_PER_PAGE', 9))
    
    # Configurações de log
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/app.log')
    
    # Configurações de email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Configurações de rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', 'memory://')
    RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', '200 per day')
    RATELIMIT_STORAGE_OPTIONS = eval(os.environ.get('RATELIMIT_STORAGE_OPTIONS', '{}'))
    
    # Configurações de cache
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))
    
    # Configurações de timezone
    TIMEZONE = TIMEZONE
    BRAZIL_TIMEZONE = 'America/Porto_Velho'
    
    # Configurações de idioma
    LANGUAGES = ['pt_BR']
    DEFAULT_LANGUAGE = 'pt_BR'
    
    # Configurações de formatação de data/hora
    DATETIME_FORMAT = '%d/%m/%Y %H:%M'
    DATE_FORMAT = '%d/%m/%Y'
    TIME_FORMAT = '%H:%M'

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    
    # Configurações específicas de desenvolvimento
    SECRET_KEY = 'dev-secret-key-change-in-production'
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    # Em produção, usar variáveis de ambiente obrigatórias
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY or SECRET_KEY == 'dev-secret-key-change-in-production':
        raise ValueError('SECRET_KEY deve ser configurada em produção!')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError('DATABASE_URL deve ser configurada em produção!')
    
    # Configurações de segurança adicionais para produção
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Headers de segurança
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' cdnjs.cloudflare.com; font-src 'self' cdnjs.cloudflare.com; img-src 'self' data:; connect-src 'self'"
    }

class TestingConfig(Config):
    """Configurações para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'

# Configuração baseada no ambiente
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 