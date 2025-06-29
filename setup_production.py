#!/usr/bin/env python3
"""
Script para configurar o ambiente de produção do Help Alphaclin
"""

import os
import secrets
import sys
from pathlib import Path

def generate_secret_key():
    """Gera uma chave secreta segura"""
    return secrets.token_hex(32)

def create_env_file():
    """Cria o arquivo .env para produção"""
    env_file = Path('.env')
    
    if env_file.exists():
        print("⚠️  Arquivo .env já existe!")
        response = input("Deseja sobrescrever? (s/N): ").lower()
        if response != 's':
            print("❌ Operação cancelada")
            return False
    
    # Gerar chave secreta
    secret_key = generate_secret_key()
    
    # Template do arquivo .env para produção
    env_content = f"""# ========================================
# CONFIGURAÇÕES DE PRODUÇÃO - HELP ALPHACLIN
# ========================================

# AMBIENTE
FLASK_ENV=production

# CONFIGURAÇÕES CRÍTICAS
SECRET_KEY={secret_key}

# Configure a URL do seu banco de dados de produção
# Exemplo PostgreSQL: postgresql://user:password@localhost/helpalphaclin
# Exemplo MySQL: mysql://user:password@localhost/helpalphaclin
DATABASE_URL=sqlite:///helpalphaclin.db

# CONFIGURAÇÕES DE SERVIDOR
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# CONFIGURAÇÕES DE SEGURANÇA
WTF_CSRF_ENABLED=True
WTF_CSRF_TIME_LIMIT=3600
PERMANENT_SESSION_LIFETIME=28800

# CONFIGURAÇÕES DE UPLOAD
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=app/uploads
DOWNLOAD_FOLDER=app/downloads

# CONFIGURAÇÕES DE PAGINAÇÃO
EXAMES_PER_PAGE=9
ADMIN_EXAMES_PER_PAGE=9

# CONFIGURAÇÕES DE LOG
LOG_LEVEL=WARNING
LOG_FILE=logs/app.log

# CONFIGURAÇÕES DE RATE LIMITING
RATELIMIT_STORAGE_URL=memory://
RATELIMIT_DEFAULT=200 per day
RATELIMIT_STORAGE_OPTIONS={{}}

# CONFIGURAÇÕES DE CACHE
CACHE_TYPE=simple
CACHE_DEFAULT_TIMEOUT=300

# ========================================
# IMPORTANTE: Configure DATABASE_URL para seu banco de produção!
# ========================================
"""
    
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✅ Arquivo .env criado com sucesso!")
        print(f"🔑 Chave secreta gerada: {secret_key[:16]}...")
        print("\n⚠️  IMPORTANTE:")
        print("1. Configure DATABASE_URL para seu banco de produção")
        print("2. Ajuste outras configurações conforme necessário")
        print("3. Mantenha o arquivo .env seguro e não o compartilhe")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar arquivo .env: {e}")
        return False

def check_production_requirements():
    """Verifica se os requisitos para produção estão atendidos"""
    print("🔍 Verificando requisitos para produção...")
    
    # Verificar se o arquivo .env existe
    if not Path('.env').exists():
        print("❌ Arquivo .env não encontrado")
        return False
    
    # Verificar variáveis críticas
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['SECRET_KEY', 'DATABASE_URL']
    missing_vars = []
    
    for var in required_vars:
        value = os.environ.get(var)
        if not value or value == 'dev-secret-key-change-in-production':
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variáveis obrigatórias não configuradas: {', '.join(missing_vars)}")
        return False
    
    print("✅ Todos os requisitos atendidos!")
    return True

def main():
    """Função principal"""
    print("🚀 Configurador de Produção - Help Alphaclin")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        check_production_requirements()
        return
    
    print("Escolha uma opção:")
    print("1. Criar arquivo .env para produção")
    print("2. Verificar requisitos de produção")
    print("3. Sair")
    
    try:
        choice = input("\nOpção: ").strip()
        
        if choice == '1':
            create_env_file()
        elif choice == '2':
            check_production_requirements()
        elif choice == '3':
            print("👋 Até logo!")
        else:
            print("❌ Opção inválida")
            
    except KeyboardInterrupt:
        print("\n👋 Operação cancelada pelo usuário")

if __name__ == '__main__':
    main() 