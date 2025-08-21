from app import create_app
from app.models import Aviso
from app.extensions import db
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Verificar se já existe um aviso de teste
    aviso_teste = Aviso.query.filter_by(titulo='AVISO DE TESTE').first()
    
    if not aviso_teste:
        # Criar um novo aviso de teste
        aviso_teste = Aviso(
            titulo='AVISO DE TESTE',
            conteudo='Este é um aviso de teste para verificar a exibição dos avisos na página inicial.',
            tipo='warning',
            is_ativo=True,
            data_inicio=datetime.utcnow(),
            data_fim=datetime.utcnow() + timedelta(days=1)
        )
        db.session.add(aviso_teste)
        db.session.commit()
        print(f'Aviso de teste criado: {aviso_teste.titulo}')
    else:
        # Garantir que o aviso existente está ativo
        aviso_teste.is_ativo = True
        aviso_teste.data_inicio = datetime.utcnow()
        aviso_teste.data_fim = datetime.utcnow() + timedelta(days=1)
        db.session.commit()
        print(f'Aviso de teste atualizado: {aviso_teste.titulo}')
    
    # Listar todos os avisos ativos
    avisos = Aviso.query.filter_by(is_ativo=True).all()
    print(f'Avisos ativos: {len(avisos)}')
    for a in avisos:
        print(f'- {a.titulo} (visível: {a.is_visible()})')