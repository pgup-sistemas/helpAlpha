#!/usr/bin/env python3
"""
Script para criar usuário administrador no Help Alphaclin
"""

import os
import sys
from datetime import datetime

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_admin_user():
    """Cria usuário administrador"""
    
    try:
        from app import create_app, init_database
        from app.models import User
        from app.extensions import db
        
        print("🔧 Criando usuário administrador...")
        
        # Criar aplicação
        app = create_app()
        
        with app.app_context():
            # Inicializar banco de dados
            init_database(app)
            
            # Verificar se já existe um usuário admin
            admin_user = User.query.filter_by(username='admin').first()
            
            if admin_user:
                print("✅ Usuário admin já existe!")
                print(f"   👤 Usuário: {admin_user.username}")
                print(f"   📧 Email: {admin_user.email}")
                print(f"   👑 Admin: {admin_user.is_admin}")
                print(f"   ✅ Ativo: {admin_user.is_active}")
                
                # Ativar se estiver inativo
                if not admin_user.is_active:
                    print("🔄 Ativando usuário admin...")
                    admin_user.is_active = True
                    admin_user.role = 'admin'
                    admin_user.set_permissions(['edit', 'delete', 'manage_users', 'view_stats'])
                    db.session.commit()
                    print("✅ Usuário admin ativado!")
            else:
                print("👤 Criando novo usuário administrador...")
                
                admin_user = User(
                    username='admin',
                    email='admin@helpalphaclin.com',
                    is_admin=True,
                    is_active=True,
                    role='admin'
                )
                admin_user.set_password('admin123')
                admin_user.set_permissions(['edit', 'delete', 'manage_users', 'view_stats'])
                admin_user.last_activity = datetime.utcnow()
                
                db.session.add(admin_user)
                db.session.commit()
                
                print("✅ Usuário administrador criado com sucesso!")
            
            # Mostrar credenciais
            print(f"\n🔐 Credenciais de acesso:")
            print(f"   👤 Usuário: admin")
            print(f"   🔑 Senha: admin123")
            print(f"   🌐 URL: /admin/login")
            
            print(f"\n⚠️  IMPORTANTE: Altere a senha padrão após o primeiro acesso!")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro ao criar usuário admin: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🚀 Help Alphaclin - Criar Usuário Admin")
    print("=" * 40)
    
    if create_admin_user():
        print("\n✅ Usuário admin criado/verificado com sucesso!")
        print("\n📖 Próximos passos:")
        print("   1. Acesse o sistema em /admin/login")
        print("   2. Faça login com as credenciais fornecidas")
        print("   3. Altere a senha padrão por segurança")
        print("   4. Configure o sistema conforme necessário")
    else:
        print("\n❌ Falha ao criar usuário admin!")
        sys.exit(1) 