import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-help-alpha-2024'
    DEBUG = True
    WTF_CSRF_ENABLED = True 