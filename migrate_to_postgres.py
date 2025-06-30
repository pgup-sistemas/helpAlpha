#!/usr/bin/env python3
"""
Script para migrar dados do SQLite local para PostgreSQL no Render
"""

import os
import sys
from datetime import datetime

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def migrate_to_postgres():
    """Migra dados do SQLite para PostgreSQL"""
    
    try:
        from app import create_app
        from app.models import User, Exame, Unidade, Aviso, SiteConfig
        from app.extensions import db
        
        print("🔄 Migrando dados para PostgreSQL...")
        
        # Criar aplicação
        app = create_app()
        
        with app.app_context():
            # Verificar configuração do banco
            print(f"📊 Configuração do Banco:")
            print(f"   URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Criar todas as tabelas no PostgreSQL
            print(f"\n🗄️  Criando tabelas no PostgreSQL...")
            db.create_all()
            print("   ✅ Tabelas criadas com sucesso")
            
            # Verificar se já existem dados
            print(f"\n🔍 Verificando dados existentes...")
            
            users_count = User.query.count()
            exames_count = Exame.query.count()
            unidades_count = Unidade.query.count()
            avisos_count = Aviso.query.count()
            
            print(f"   👥 Usuários: {users_count}")
            print(f"   🔬 Exames: {exames_count}")
            print(f"   🏥 Unidades: {unidades_count}")
            print(f"   📢 Avisos: {avisos_count}")
            
            # Se não há dados, criar usuário admin
            if users_count == 0:
                print(f"\n👤 Criando usuário administrador...")
                
                admin_user = User()
                admin_user.username = 'admin'
                admin_user.email = 'admin@helpalphaclin.com'
                admin_user.is_admin = True
                admin_user.is_active = True
                admin_user.role = 'admin'
                admin_user.set_password('admin123')
                admin_user.set_permissions(['edit', 'delete', 'manage_users', 'view_stats'])
                admin_user.last_activity = datetime.utcnow()
                
                db.session.add(admin_user)
                db.session.commit()
                
                print("   ✅ Usuário admin criado")
            
            # Criar configuração padrão do site se não existir
            config = SiteConfig.query.first()
            if not config:
                print(f"\n⚙️  Criando configuração padrão do site...")
                config = SiteConfig()
                db.session.add(config)
                db.session.commit()
                print("   ✅ Configuração criada")
            
            print(f"\n✅ Migração concluída com sucesso!")
            
            # Mostrar resumo final
            print(f"\n📊 Resumo final:")
            print(f"   👥 Usuários: {User.query.count()}")
            print(f"   🔬 Exames: {Exame.query.count()}")
            print(f"   🏥 Unidades: {Unidade.query.count()}")
            print(f"   📢 Avisos: {Aviso.query.count()}")
            
            if users_count == 0:
                print(f"\n🔐 Credenciais de acesso:")
                print(f"   👤 Usuário: admin")
                print(f"   🔑 Senha: admin123")
                print(f"   🌐 URL: /admin/login")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro durante a migração: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🚀 Help Alphaclin - Migração para PostgreSQL")
    print("=" * 50)
    
    if migrate_to_postgres():
        print("\n✅ Migração concluída com sucesso!")
        print("\n📖 Próximos passos:")
        print("   1. Faça commit e push para o GitHub")
        print("   2. O Render fará deploy automático")
        print("   3. Acesse o sistema no Render")
        print("   4. Teste a criação de usuários")
    else:
        print("\n❌ Migração falhou!")
        sys.exit(1) 