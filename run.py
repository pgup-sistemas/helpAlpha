#!/usr/bin/env python3
"""
Script principal para executar a aplicação Flask
"""

import os
import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
from app import create_app, init_database
from config import config

# Detectar ambiente automaticamente
def get_config():
    """Detecta e retorna a configuração apropriada"""
    env = os.environ.get('FLASK_ENV', 'development')
    
    # Em produção, verificar variáveis de ambiente críticas
    if env == 'production':
        required_vars = ['SECRET_KEY', 'DATABASE_URL']
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        if missing_vars:
            print(f"❌ Variáveis de ambiente obrigatórias não configuradas: {', '.join(missing_vars)}")
            print("💡 Configure as variáveis de ambiente ou use FLASK_ENV=development para desenvolvimento")
            return config['development']
    
    return config.get(env, config['default'])

# Criar aplicação com configuração apropriada
config_class = get_config()
app = create_app(config_class)

# Inicializar banco de dados
init_database(app)

if __name__ == '__main__':
    # Configurações de execução baseadas no ambiente
    debug = config_class.DEBUG if hasattr(config_class, 'DEBUG') else True
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    print(f"🚀 Iniciando Help Alphaclin em modo {'DESENVOLVIMENTO' if debug else 'PRODUÇÃO'}")
    print(f"🌐 Servidor rodando em: http://{host}:{port}")
    print(f"🔧 Debug: {'Ativado' if debug else 'Desativado'}")
    
    app.run(debug=debug, host=host, port=port)