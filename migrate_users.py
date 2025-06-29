#!/usr/bin/env python3
"""
Script para migrar o banco de dados e adicionar sistema de usuários
"""

import os
import sys
from datetime import datetime

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, init_database
from app.extensions import db
from app.models import User
from sqlalchemy import text

def migrate_users():
    """Migra o banco de dados para adicionar campos de usuário"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Iniciando migração do sistema de usuários...")
        
        try:
            # Verificar se os novos campos já existem
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('user')]
            
            if 'role' in columns and 'permissions' in columns and 'last_activity' in columns:
                print("✅ Campos de usuário já existem no banco de dados")
                return True
            
            # Adicionar novos campos se não existirem
            print("📝 Adicionando novos campos ao modelo User...")
            
            # Executar migração manual
            with db.engine.connect() as conn:
                # Adicionar coluna role se não existir
                if 'role' not in columns:
                    conn.execute(text("ALTER TABLE user ADD COLUMN role VARCHAR(20) DEFAULT 'viewer'"))
                    print("  ✅ Coluna 'role' adicionada")
                
                # Adicionar coluna permissions se não existir
                if 'permissions' not in columns:
                    conn.execute(text("ALTER TABLE user ADD COLUMN permissions TEXT DEFAULT '[]'"))
                    print("  ✅ Coluna 'permissions' adicionada")
                
                # Adicionar coluna last_activity se não existir
                if 'last_activity' not in columns:
                    conn.execute(text("ALTER TABLE user ADD COLUMN last_activity DATETIME"))
                    print("  ✅ Coluna 'last_activity' adicionada")
                
                conn.commit()
            
            # Atualizar usuários existentes
            print("👥 Atualizando usuários existentes...")
            
            # Buscar todos os usuários
            users = User.query.all()
            
            for user in users:
                # Definir role baseado em is_admin
                if user.is_admin:
                    user.role = 'admin'
                    user.set_permissions(['edit', 'delete', 'manage_users', 'view_stats'])
                else:
                    user.role = 'viewer'
                    user.set_permissions(['view_stats'])
                
                # Definir última atividade como data de criação
                if not user.last_activity:
                    user.last_activity = user.created_at or datetime.utcnow()
            
            db.session.commit()
            print(f"  ✅ {len(users)} usuários atualizados")
            
            print("🎉 Migração concluída com sucesso!")
            
            # Mostrar resumo
            print("\n📊 Resumo da migração:")
            admin_count = User.query.filter_by(role='admin').count()
            editor_count = User.query.filter_by(role='editor').count()
            viewer_count = User.query.filter_by(role='viewer').count()
            
            print(f"  👑 Administradores: {admin_count}")
            print(f"  ✏️  Editores: {editor_count}")
            print(f"  👁️  Visualizadores: {viewer_count}")
            
        except Exception as e:
            print(f"❌ Erro durante a migração: {e}")
            db.session.rollback()
            return False
        
        return True

def create_sample_users():
    """Cria usuários de exemplo para teste"""
    app = create_app()
    
    with app.app_context():
        print("\n👥 Criando usuários de exemplo...")
        
        # Verificar se já existem usuários além do admin
        user_count = User.query.count()
        if user_count > 1:
            print("  ℹ️  Usuários já existem, pulando criação de exemplos")
            return
        
        # Criar usuário editor
        editor = User(
            username='editor',
            email='editor@helpalphaclin.com',
            role='editor',
            is_admin=False,
            is_active=True
        )
        editor.set_password('editor123')
        editor.set_permissions(['edit', 'view_stats'])
        
        # Criar usuário viewer
        viewer = User(
            username='viewer',
            email='viewer@helpalphaclin.com',
            role='viewer',
            is_admin=False,
            is_active=True
        )
        viewer.set_password('viewer123')
        viewer.set_permissions(['view_stats'])
        
        try:
            db.session.add(editor)
            db.session.add(viewer)
            db.session.commit()
            
            print("  ✅ Usuário editor criado: editor / editor123")
            print("  ✅ Usuário viewer criado: viewer / viewer123")
            
        except Exception as e:
            print(f"  ❌ Erro ao criar usuários de exemplo: {e}")
            db.session.rollback()

if __name__ == '__main__':
    print("🚀 Sistema de Gerenciamento de Usuários - Help Alphaclin")
    print("=" * 60)
    
    # Executar migração
    if migrate_users():
        # Criar usuários de exemplo
        create_sample_users()
        
        print("\n✅ Migração concluída!")
        print("\n📋 Próximos passos:")
        print("  1. Teste o login com os usuários criados")
        print("  2. Acesse /admin/usuarios para gerenciar usuários")
        print("  3. Verifique as permissões de cada nível de acesso")
        print("\n🔐 Credenciais de teste:")
        print("  👑 Admin: admin / admin123")
        print("  ✏️  Editor: editor / editor123")
        print("  👁️  Viewer: viewer / viewer123")
    else:
        print("\n❌ Migração falhou!")
        sys.exit(1) 