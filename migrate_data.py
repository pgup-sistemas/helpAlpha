#!/usr/bin/env python3
"""
Script de migração e inicialização do banco de dados
Help Alphaclin - Sistema de consulta de exames

Este script:
1. Cria todas as tabelas do banco de dados
2. Cria um usuário administrador padrão
3. Cria configurações básicas do site
4. Opcionalmente carrega dados de exemplo

Uso:
    python migrate_data.py
    python migrate_data.py --with-examples
"""

import os
import sys
from datetime import datetime
import json

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models import User, SiteConfig, Exame, Unidade, Aviso

def create_admin_user():
    """Cria o usuário administrador padrão"""
    print("Criando usuário administrador...")
    
    # Verificar se já existe um admin
    admin = User.query.filter_by(is_admin=True).first()
    if admin:
        print(f"Usuário administrador já existe: {admin.username}")
        return admin
    
    # Criar novo admin
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@alphaclin.com')
    admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    admin = User(
        username=admin_username,
        email=admin_email,
        is_admin=True,
        role='admin',
        is_active=True
    )
    admin.set_password(admin_password)
    admin.set_permissions(['edit', 'delete', 'manage_users', 'view_stats'])
    
    db.session.add(admin)
    db.session.commit()
    
    print(f"Usuário administrador criado:")
    print(f"  Username: {admin_username}")
    print(f"  Email: {admin_email}")
    print(f"  Password: {admin_password}")
    print("  IMPORTANTE: Altere a senha após o primeiro login!")
    
    return admin

def create_site_config():
    """Cria as configurações básicas do site"""
    print("Criando configurações do site...")
    
    # Verificar se já existe configuração
    config = SiteConfig.query.first()
    if config:
        print("Configurações do site já existem")
        return config
    
    # Criar configuração padrão
    config = SiteConfig(
        nome_site='Help Alphaclin',
        descricao_site='Sistema de consulta de exames laboratoriais e de imagem',
        email_contato=os.getenv('COMPANY_EMAIL', 'contato@alphaclin.com'),
        telefone_principal=os.getenv('COMPANY_PHONE', '(11) 1234-5678'),
        whatsapp=os.getenv('COMPANY_WHATSAPP', '5511123456789'),
        meta_description='Consulte informações sobre exames laboratoriais e de imagem. Preparos, documentos necessários e orientações pós-exame.',
        meta_keywords='exames, laboratório, imagem, preparo, alphaclin',
        cor_primaria='#667eea',
        cor_secundaria='#764ba2',
        mostrar_contatos=True,
        mostrar_mapa=True,
        mostrar_redes_sociais=True
    )
    
    # Configurar endereços padrão
    enderecos_padrao = [
        {
            'nome': 'Unidade Principal',
            'endereco': 'Rua Principal, 123 - Centro',
            'cidade': 'São Paulo',
            'cep': '01234-567',
            'telefone': '(11) 1234-5678'
        }
    ]
    config.set_enderecos(enderecos_padrao)
    
    # Configurar horários padrão
    horarios_padrao = {
        'segunda': '07:00 - 17:00',
        'terca': '07:00 - 17:00',
        'quarta': '07:00 - 17:00',
        'quinta': '07:00 - 17:00',
        'sexta': '07:00 - 17:00',
        'sabado': '07:00 - 12:00',
        'domingo': 'Fechado'
    }
    config.set_horarios_funcionamento(horarios_padrao)
    
    # Configurar informações importantes
    info_importantes = [
        'Trazer documento com foto',
        'Chegar com 30 minutos de antecedência',
        'Seguir orientações de preparo'
    ]
    config.set_informacoes_importantes(info_importantes)
    
    db.session.add(config)
    db.session.commit()
    
    print("Configurações do site criadas com sucesso")
    return config

def create_example_data():
    """Cria dados de exemplo (exames, unidades, avisos)"""
    print("Criando dados de exemplo...")
    
    # Exames de exemplo
    exames_exemplo = [
        {
            'nome': 'Hemograma Completo',
            'descricao': 'Exame que avalia as células do sangue: glóbulos vermelhos, glóbulos brancos e plaquetas.',
            'preparo': 'Jejum de 4 horas. Pode beber água.',
            'documentos': 'RG, CPF e carteirinha do convênio (se houver).',
            'pos_exame': 'Pode retomar alimentação normal imediatamente após a coleta.',
            'tempo': '15 minutos',
            'categoria': 'laboratorio',
            'icone': 'fas fa-flask'
        },
        {
            'nome': 'Raio-X de Tórax',
            'descricao': 'Exame de imagem para avaliar pulmões, coração e estruturas do tórax.',
            'preparo': 'Não é necessário preparo específico. Retirar objetos metálicos.',
            'documentos': 'RG, CPF, carteirinha do convênio e pedido médico.',
            'pos_exame': 'Não há restrições após o exame.',
            'tempo': '10 minutos',
            'categoria': 'imagem',
            'icone': 'fas fa-x-ray'
        },
        {
            'nome': 'Vacina da Gripe',
            'descricao': 'Imunização contra influenza (gripe).',
            'preparo': 'Não estar com febre ou sintomas gripais.',
            'documentos': 'RG, CPF e carteira de vacinação.',
            'pos_exame': 'Observar local da aplicação por 30 minutos. Evitar exercícios intensos no dia.',
            'tempo': '5 minutos',
            'categoria': 'vacina',
            'icone': 'fas fa-syringe'
        }
    ]
    
    for exame_data in exames_exemplo:
        # Verificar se já existe
        exame_existente = Exame.query.filter_by(nome=exame_data['nome']).first()
        if not exame_existente:
            exame = Exame(**exame_data)
            db.session.add(exame)
    
    # Unidade de exemplo
    unidade_existente = Unidade.query.first()
    if not unidade_existente:
        unidade = Unidade(
            nome='Unidade Principal',
            endereco='Rua Principal, 123 - Centro\nSão Paulo - SP\nCEP: 01234-567',
            telefones='(11) 1234-5678, (11) 9876-5432',
            horarios=json.dumps({
                'segunda_sexta': '07:00 - 17:00',
                'sabado': '07:00 - 12:00',
                'domingo': 'Fechado'
            }),
            coordenadas='-23.5505,-46.6333',  # São Paulo
            is_ativo=True
        )
        db.session.add(unidade)
    
    # Aviso de exemplo
    aviso_existente = Aviso.query.first()
    if not aviso_existente:
        aviso = Aviso(
            titulo='Bem-vindo ao Help Alphaclin',
            conteudo='Sistema de consulta de exames laboratoriais e de imagem. Consulte as informações sobre preparos e documentos necessários.',
            tipo='info',
            is_ativo=True
        )
        db.session.add(aviso)
    
    db.session.commit()
    print("Dados de exemplo criados com sucesso")

def main():
    """Função principal do script de migração"""
    print("=== Help Alphaclin - Script de Migração ===")
    print(f"Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Verificar argumentos
    with_examples = '--with-examples' in sys.argv
    
    # Criar aplicação Flask
    app = create_app()
    
    with app.app_context():
        try:
            print("\n1. Criando tabelas do banco de dados...")
            db.create_all()
            print("Tabelas criadas com sucesso!")
            
            print("\n2. Criando usuário administrador...")
            create_admin_user()
            
            print("\n3. Criando configurações do site...")
            create_site_config()
            
            if with_examples:
                print("\n4. Criando dados de exemplo...")
                create_example_data()
            else:
                print("\n4. Dados de exemplo não solicitados (use --with-examples para incluir)")
            
            print("\n=== Migração concluída com sucesso! ===")
            print("\nPróximos passos:")
            print("1. Acesse o sistema com as credenciais do administrador")
            print("2. Altere a senha padrão")
            print("3. Configure as informações da empresa")
            print("4. Adicione os exames do seu laboratório")
            print("5. Teste todas as funcionalidades")
            
            if not with_examples:
                print("\nPara adicionar dados de exemplo, execute:")
                print("python migrate_data.py --with-examples")
            
        except Exception as e:
            print(f"\nERRO durante a migração: {e}")
            print("Verifique:")
            print("- Se o banco de dados está acessível")
            print("- Se as variáveis de ambiente estão configuradas")
            print("- Se não há conflitos de dados existentes")
            sys.exit(1)

if __name__ == '__main__':
    main()
