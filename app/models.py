from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime, timedelta
import json

# Importar a instância do db do extensions.py
from app.extensions import db

class User(UserMixin, db.Model):
    """Modelo de usuário para autenticação"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), default='viewer')  # admin, editor, viewer
    permissions = db.Column(db.Text, default='[]')  # JSON com permissões específicas
    last_activity = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relacionamento com tokens de redefinição
    reset_tokens = db.relationship('PasswordResetToken', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Define a senha do usuário"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.password_hash, password)
    
    def get_permissions(self):
        """Retorna lista de permissões do usuário"""
        try:
            return json.loads(self.permissions)
        except (json.JSONDecodeError, TypeError):
            return []
    
    def set_permissions(self, permissions_list):
        """Define as permissões do usuário"""
        self.permissions = json.dumps(permissions_list)
    
    def has_permission(self, permission):
        """Verifica se o usuário tem uma permissão específica"""
        if self.is_admin:
            return True
        return permission in self.get_permissions()
    
    def can_edit(self):
        """Verifica se o usuário pode editar conteúdo"""
        return self.is_admin or self.role in ['admin', 'editor'] or 'edit' in self.get_permissions()
    
    def can_delete(self):
        """Verifica se o usuário pode deletar conteúdo"""
        return self.is_admin or 'delete' in self.get_permissions()
    
    def can_manage_users(self):
        """Verifica se o usuário pode gerenciar outros usuários"""
        return self.is_admin or 'manage_users' in self.get_permissions()
    
    def update_activity(self):
        """Atualiza a última atividade do usuário"""
        self.last_activity = datetime.utcnow()
        db.session.commit()
    
    def generate_reset_token(self):
        """Gera um token para redefinição de senha"""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=24)  # Token válido por 24 horas
        
        reset_token = PasswordResetToken(
            token=token,
            user_id=self.id,
            expires_at=expires_at
        )
        
        db.session.add(reset_token)
        db.session.commit()
        
        return token
    
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'

class PasswordResetToken(db.Model):
    """Modelo para tokens de redefinição de senha"""
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def is_valid(self):
        """Verifica se o token ainda é válido"""
        return not self.used and datetime.utcnow() < self.expires_at
    
    def mark_as_used(self):
        """Marca o token como usado"""
        self.used = True
        db.session.commit()
    
    def __repr__(self):
        return f'<PasswordResetToken {self.token[:10]}...>'

class Exame(db.Model):
    """Modelo para exames no banco de dados"""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), unique=True, nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preparo = db.Column(db.Text, nullable=False)
    documentos = db.Column(db.Text, nullable=False)
    pos_exame = db.Column(db.Text, nullable=False)
    tempo = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(20), nullable=False, default='laboratorio')  # laboratorio, imagem, vacina
    icone = db.Column(db.String(50), default='fas fa-flask')  # Ícone personalizado
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com estatísticas
    estatisticas = db.relationship('EstatisticaExame', backref='exame', lazy=True, cascade='all, delete-orphan')
    
    @property
    def categoria_display(self):
        """Retorna o nome da categoria para exibição"""
        categorias = {
            'laboratorio': 'Laboratório',
            'imagem': 'Exame de Imagem',
            'vacina': 'Vacina'
        }
        return categorias.get(self.categoria, self.categoria.title())
    
    @property
    def icone_padrao(self):
        """Retorna o ícone padrão baseado na categoria"""
        icones = {
            'laboratorio': 'fas fa-flask',
            'imagem': 'fas fa-x-ray',
            'vacina': 'fas fa-syringe'
        }
        return icones.get(self.categoria, 'fas fa-stethoscope')
    
    @property
    def cor_categoria(self):
        """Retorna a cor da categoria para uso em CSS"""
        cores = {
            'laboratorio': 'is-info',
            'imagem': 'is-warning',
            'vacina': 'is-success'
        }
        return cores.get(self.categoria, 'is-primary')
    
    def to_dict(self):
        """Converte o exame para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preparo': self.preparo,
            'documentos': self.documentos,
            'pos_exame': self.pos_exame,
            'tempo': self.tempo,
            'categoria': self.categoria,
            'categoria_display': self.categoria_display,
            'icone': self.icone or self.icone_padrao,
            'cor_categoria': self.cor_categoria,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Exame {self.nome} ({self.categoria})>'

class Unidade(db.Model):
    """Modelo para unidades da empresa"""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.Text, nullable=False)
    telefones = db.Column(db.Text, nullable=False)  # JSON string ou texto separado por vírgulas
    horarios = db.Column(db.Text, nullable=False)   # JSON string com horários
    coordenadas = db.Column(db.String(100))  # Latitude,Longitude (opcional)
    is_ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Converte a unidade para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'endereco': self.endereco,
            'telefones': self.telefones,
            'horarios': self.horarios,
            'coordenadas': self.coordenadas,
            'is_ativo': self.is_ativo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Unidade {self.nome}>'

class Aviso(db.Model):
    """Modelo para avisos do sistema"""
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(20), default='info')  # info, warning, error, success
    is_ativo = db.Column(db.Boolean, default=True)
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime)  # None = sem data de expiração
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def is_visible(self):
        """Verifica se o aviso deve ser exibido"""
        now = datetime.utcnow()
        if not self.is_ativo:
            return False
        if self.data_inicio and now < self.data_inicio:
            return False
        if self.data_fim and now > self.data_fim:
            return False
        return True
    
    def to_dict(self):
        """Converte o aviso para dicionário"""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'conteudo': self.conteudo,
            'tipo': self.tipo,
            'is_ativo': self.is_ativo,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim': self.data_fim.isoformat() if self.data_fim else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Aviso {self.titulo}>'

class LogAcesso(db.Model):
    """Modelo para logs de acesso ao sistema"""
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=False)  # Suporte para IPv6
    user_agent = db.Column(db.Text)
    pagina = db.Column(db.String(100), nullable=False)  # /, /exame/nome, etc.
    metodo = db.Column(db.String(10), nullable=False)  # GET, POST, etc.
    status_code = db.Column(db.Integer, nullable=False)
    tempo_resposta = db.Column(db.Float)  # Tempo em segundos
    query_string = db.Column(db.Text)  # Parâmetros da URL
    referrer = db.Column(db.Text)  # Página de origem
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LogAcesso {self.ip_address} - {self.pagina} - {self.created_at}>'

class EstatisticaExame(db.Model):
    """Modelo para estatísticas de consulta de exames"""
    id = db.Column(db.Integer, primary_key=True)
    exame_id = db.Column(db.Integer, db.ForeignKey('exame.id'), nullable=False)
    tipo_consulta = db.Column(db.String(20), nullable=False)  # 'busca', 'visualizacao'
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    query_busca = db.Column(db.String(200))  # Termo de busca usado
    tempo_visualizacao = db.Column(db.Integer)  # Tempo em segundos (se aplicável)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EstatisticaExame {self.exame_id} - {self.tipo_consulta} - {self.created_at}>'

class EstatisticaBusca(db.Model):
    """Modelo para estatísticas de buscas realizadas"""
    id = db.Column(db.Integer, primary_key=True)
    termo_busca = db.Column(db.String(200), nullable=False)
    resultados_encontrados = db.Column(db.Integer, nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EstatisticaBusca {self.termo_busca} - {self.created_at}>'

class SiteConfig(db.Model):
    """Modelo para configurações gerais do site"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Informações básicas
    nome_site = db.Column(db.String(100), nullable=False, default='Help Alphaclin')
    descricao_site = db.Column(db.Text, nullable=False, default='Sistema de consulta de exames laboratoriais e de imagem')
    email_contato = db.Column(db.String(100))
    telefone_principal = db.Column(db.String(20))
    whatsapp = db.Column(db.String(20))
    
    # Endereços (JSON)
    enderecos = db.Column(db.Text, nullable=False, default='[]')  # Lista de endereços em JSON
    
    # Redes sociais (JSON)
    redes_sociais = db.Column(db.Text, nullable=False, default='[]')  # Lista de redes sociais em JSON
    
    # Mapa do Google
    google_maps_api_key = db.Column(db.String(200))
    google_maps_embed_url = db.Column(db.Text)
    
    # Horários de funcionamento
    horarios_funcionamento = db.Column(db.Text, nullable=False, default='{}')  # JSON com horários
    
    # Informações adicionais
    informacoes_importantes = db.Column(db.Text, nullable=False, default='[]')  # Lista de informações em JSON
    
    # SEO e meta tags
    meta_keywords = db.Column(db.Text)
    meta_description = db.Column(db.Text)
    
    # Configurações de tema
    cor_primaria = db.Column(db.String(7), default='#667eea')  # Hex color
    cor_secundaria = db.Column(db.String(7), default='#764ba2')  # Hex color
    
    # Configurações de contato
    mostrar_contatos = db.Column(db.Boolean, default=True)
    mostrar_mapa = db.Column(db.Boolean, default=True)
    mostrar_redes_sociais = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_enderecos(self):
        """Retorna a lista de endereços como dicionário"""
        try:
            return json.loads(self.enderecos) if self.enderecos else []
        except:
            return []
    
    def set_enderecos(self, enderecos_list):
        """Define a lista de endereços"""
        self.enderecos = json.dumps(enderecos_list, ensure_ascii=False)
    
    def get_redes_sociais(self):
        """Retorna a lista de redes sociais como dicionário"""
        try:
            return json.loads(self.redes_sociais) if self.redes_sociais else []
        except:
            return []
    
    def set_redes_sociais(self, redes_list):
        """Define a lista de redes sociais"""
        self.redes_sociais = json.dumps(redes_list, ensure_ascii=False)
    
    def get_horarios_funcionamento(self):
        """Retorna os horários de funcionamento como dicionário"""
        try:
            return json.loads(self.horarios_funcionamento) if self.horarios_funcionamento else {}
        except:
            return {}
    
    def set_horarios_funcionamento(self, horarios_dict):
        """Define os horários de funcionamento"""
        self.horarios_funcionamento = json.dumps(horarios_dict, ensure_ascii=False)
    
    def get_informacoes_importantes(self):
        """Retorna as informações importantes como lista"""
        try:
            return json.loads(self.informacoes_importantes) if self.informacoes_importantes else []
        except:
            return []
    
    def set_informacoes_importantes(self, informacoes_list):
        """Define as informações importantes"""
        self.informacoes_importantes = json.dumps(informacoes_list, ensure_ascii=False)
    
    def to_dict(self):
        """Converte as configurações para dicionário"""
        return {
            'id': self.id,
            'nome_site': self.nome_site,
            'descricao_site': self.descricao_site,
            'email_contato': self.email_contato,
            'telefone_principal': self.telefone_principal,
            'whatsapp': self.whatsapp,
            'enderecos': self.get_enderecos(),
            'redes_sociais': self.get_redes_sociais(),
            'google_maps_api_key': self.google_maps_api_key,
            'google_maps_embed_url': self.google_maps_embed_url,
            'horarios_funcionamento': self.get_horarios_funcionamento(),
            'informacoes_importantes': self.get_informacoes_importantes(),
            'meta_keywords': self.meta_keywords,
            'meta_description': self.meta_description,
            'cor_primaria': self.cor_primaria,
            'cor_secundaria': self.cor_secundaria,
            'mostrar_contatos': self.mostrar_contatos,
            'mostrar_mapa': self.mostrar_mapa,
            'mostrar_redes_sociais': self.mostrar_redes_sociais,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<SiteConfig {self.nome_site}>' 