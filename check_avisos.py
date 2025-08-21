from app import create_app
from app.models import Aviso
from datetime import datetime
import pytz

app = create_app()

with app.app_context():
    # Verificar avisos ativos
    agora = datetime.now(pytz.UTC)
    avisos = Aviso.query.filter(
        Aviso.is_ativo == True,
        Aviso.data_inicio <= agora,
        (Aviso.data_fim.is_(None) | (Aviso.data_fim >= agora))
    ).all()
    
    print(f'Avisos ativos encontrados: {len(avisos)}')
    for aviso in avisos:
        print(f'- {aviso.titulo}: {aviso.conteudo}')
        print(f'  Ativo desde: {aviso.data_inicio}')
        if aviso.data_fim:
            print(f'  Válido até: {aviso.data_fim}')
        print()