from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, Unidade, Aviso
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[
        DataRequired(message='O nome de usuário é obrigatório'),
        Length(min=3, max=80, message='O usuário deve ter entre 3 e 80 caracteres')
    ])
    password = PasswordField('Senha', validators=[
        DataRequired(message='A senha é obrigatória')
    ])
    submit = SubmitField('Entrar')

class ExameForm(FlaskForm):
    nome = StringField('Nome do Exame', validators=[
        DataRequired(message='O nome do exame é obrigatório'),
        Length(min=3, max=100, message='O nome deve ter entre 3 e 100 caracteres')
    ])
    descricao = TextAreaField('Descrição', validators=[
        DataRequired(message='A descrição é obrigatória'),
        Length(min=10, max=500, message='A descrição deve ter entre 10 e 500 caracteres')
    ])
    preparo = TextAreaField('Preparo Necessário', validators=[
        DataRequired(message='O preparo é obrigatório'),
        Length(min=5, max=1000, message='O preparo deve ter entre 5 e 1000 caracteres')
    ])
    documentos = TextAreaField('Documentos Exigidos', validators=[
        DataRequired(message='Os documentos exigidos são obrigatórios'),
        Length(min=5, max=200, message='Os documentos devem ter entre 5 e 200 caracteres')
    ])
    pos_exame = TextAreaField('Cuidados Após o Exame', validators=[
        DataRequired(message='Os cuidados após o exame são obrigatórios'),
        Length(min=5, max=1000, message='Os cuidados devem ter entre 5 e 1000 caracteres')
    ])
    tempo = StringField('Duração', validators=[
        DataRequired(message='A duração é obrigatória'),
        Length(min=2, max=50, message='A duração deve ter entre 2 e 50 caracteres')
    ])
    categoria = SelectField('Categoria', choices=[
        ('laboratorio', 'Laboratório'),
        ('imagem', 'Exame de Imagem'),
        ('vacina', 'Vacina')
    ], validators=[DataRequired(message='A categoria é obrigatória')], 
    description='Selecione a categoria do serviço')
    icone = StringField('Ícone Personalizado (opcional)', validators=[
        Length(max=50, message='O ícone deve ter no máximo 50 caracteres')
    ], description='Ex: fas fa-heart, fas fa-brain. Deixe em branco para usar o ícone padrão da categoria')
    submit = SubmitField('Salvar Exame')

class UploadExcelForm(FlaskForm):
    arquivo = FileField('Arquivo Excel', validators=[
        DataRequired(message='Selecione um arquivo Excel para importar'),
        FileAllowed(['xlsx', 'xls'], message='Apenas arquivos Excel (.xlsx, .xls) são permitidos')
    ])
    submit = SubmitField('Importar Exames')

class PasswordResetRequestForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[
        DataRequired(message='O nome de usuário é obrigatório'),
        Length(min=3, max=80, message='O usuário deve ter entre 3 e 80 caracteres')
    ])
    submit = SubmitField('Solicitar Redefinição')
    
    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if not user:
            raise ValidationError('Usuário não encontrado.')
        if not user.is_active:
            raise ValidationError('Usuário inativo.')

class PasswordResetForm(FlaskForm):
    password = PasswordField('Nova Senha', validators=[
        DataRequired(message='A nova senha é obrigatória'),
        Length(min=6, message='A senha deve ter pelo menos 6 caracteres')
    ])
    confirm_password = PasswordField('Confirmar Nova Senha', validators=[
        DataRequired(message='A confirmação da senha é obrigatória'),
        EqualTo('password', message='As senhas devem ser iguais')
    ])
    submit = SubmitField('Redefinir Senha')

class UserForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[
        DataRequired(message='O nome de usuário é obrigatório'),
        Length(min=3, max=80, message='O usuário deve ter entre 3 e 80 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='O email é obrigatório'),
        Email(message='Digite um email válido')
    ])
    password = PasswordField('Senha', validators=[
        Length(min=6, message='A senha deve ter pelo menos 6 caracteres')
    ])
    confirm_password = PasswordField('Confirmar Senha', validators=[
        EqualTo('password', message='As senhas devem ser iguais')
    ])
    role = SelectField('Nível de Acesso', choices=[
        ('viewer', 'Visualizador'),
        ('editor', 'Editor'),
        ('admin', 'Administrador')
    ], validators=[DataRequired(message='Selecione um nível de acesso')])
    is_admin = BooleanField('É Administrador')
    is_active = BooleanField('Usuário Ativo')
    submit = SubmitField('Salvar Usuário')
    
    def __init__(self, original_username=None, original_email=None, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
    
    def validate_username(self, field):
        if field.data != self.original_username:
            user = User.query.filter_by(username=field.data).first()
            if user:
                raise ValidationError('Este nome de usuário já está em uso.')
    
    def validate_email(self, field):
        if field.data != self.original_email:
            user = User.query.filter_by(email=field.data).first()
            if user:
                raise ValidationError('Este email já está em uso.')
    
    def validate_password(self, field):
        # Senha é obrigatória apenas para novos usuários
        if not self.original_username and not field.data:
            raise ValidationError('A senha é obrigatória para novos usuários.')

class UnidadeForm(FlaskForm):
    nome = StringField('Nome da Unidade', validators=[
        DataRequired(message='O nome da unidade é obrigatório'),
        Length(min=3, max=100, message='O nome deve ter entre 3 e 100 caracteres')
    ])
    endereco = TextAreaField('Endereço', validators=[
        DataRequired(message='O endereço é obrigatório'),
        Length(min=10, max=300, message='O endereço deve ter entre 10 e 300 caracteres')
    ])
    telefones = TextAreaField('Telefones', validators=[
        DataRequired(message='Os telefones são obrigatórios'),
        Length(min=5, max=200, message='Os telefones devem ter entre 5 e 200 caracteres')
    ], description='Digite os telefones separados por vírgula ou quebra de linha')
    horarios = TextAreaField('Horários de Funcionamento', validators=[
        DataRequired(message='Os horários são obrigatórios'),
        Length(min=10, max=500, message='Os horários devem ter entre 10 e 500 caracteres')
    ], description='Digite os horários de funcionamento')
    coordenadas = StringField('Coordenadas (Latitude,Longitude)', validators=[
        Length(max=100, message='As coordenadas devem ter no máximo 100 caracteres')
    ], description='Ex: -8.7619,-63.9039 (opcional)')
    is_ativo = BooleanField('Unidade Ativa', default=True)
    submit = SubmitField('Salvar Unidade')
    
    def __init__(self, original_nome=None, *args, **kwargs):
        super(UnidadeForm, self).__init__(*args, **kwargs)
        self.original_nome = original_nome
    
    def validate_nome(self, field):
        if field.data != self.original_nome:
            unidade = Unidade.query.filter_by(nome=field.data).first()
            if unidade:
                raise ValidationError('Já existe uma unidade com este nome.')

class AvisoForm(FlaskForm):
    titulo = StringField('Título do Aviso', validators=[
        DataRequired(message='O título é obrigatório'),
        Length(min=5, max=200, message='O título deve ter entre 5 e 200 caracteres')
    ])
    conteudo = TextAreaField('Conteúdo', validators=[
        DataRequired(message='O conteúdo é obrigatório'),
        Length(min=10, max=1000, message='O conteúdo deve ter entre 10 e 1000 caracteres')
    ])
    tipo = SelectField('Tipo de Aviso', choices=[
        ('info', 'Informação'),
        ('warning', 'Aviso'),
        ('error', 'Erro'),
        ('success', 'Sucesso')
    ], validators=[DataRequired(message='O tipo de aviso é obrigatório')])
    is_ativo = BooleanField('Aviso Ativo', default=True)
    data_inicio = DateTimeField('Data de Início', format='%Y-%m-%dT%H:%M', 
                               default=datetime.utcnow, validators=[
                                   DataRequired(message='A data de início é obrigatória')
                               ])
    data_fim = DateTimeField('Data de Fim (Opcional)', format='%Y-%m-%dT%H:%M', 
                            description='Deixe em branco para aviso permanente')
    submit = SubmitField('Salvar Aviso')

class SiteConfigForm(FlaskForm):
    # Informações básicas
    nome_site = StringField('Nome do Site', validators=[
        DataRequired(message='O nome do site é obrigatório'),
        Length(min=3, max=100, message='O nome deve ter entre 3 e 100 caracteres')
    ])
    descricao_site = TextAreaField('Descrição do Site', validators=[
        DataRequired(message='A descrição do site é obrigatória'),
        Length(min=10, max=500, message='A descrição deve ter entre 10 e 500 caracteres')
    ])
    email_contato = StringField('Email de Contato', validators=[
        Email(message='Digite um email válido')
    ])
    telefone_principal = StringField('Telefone Principal', validators=[
        Length(max=20, message='O telefone deve ter no máximo 20 caracteres')
    ])
    whatsapp = StringField('WhatsApp', validators=[
        Length(max=20, message='O WhatsApp deve ter no máximo 20 caracteres')
    ])
    
    # Mapa do Google
    google_maps_api_key = StringField('Chave da API do Google Maps', validators=[
        Length(max=200, message='A chave da API deve ter no máximo 200 caracteres')
    ], description='Chave da API do Google Maps (opcional)')
    google_maps_embed_url = TextAreaField('URL de Incorporação do Google Maps', 
                                         description='URL completa do iframe do Google Maps')
    
    # SEO e meta tags
    meta_keywords = TextAreaField('Palavras-chave (Meta Keywords)', 
                                 description='Palavras-chave separadas por vírgula')
    meta_description = TextAreaField('Descrição (Meta Description)', 
                                    validators=[
                                        Length(max=160, message='A descrição deve ter no máximo 160 caracteres')
                                    ],
                                    description='Descrição para SEO (máximo 160 caracteres)')
    
    # Configurações de tema
    cor_primaria = StringField('Cor Primária', validators=[
        Length(max=7, message='A cor deve ter no máximo 7 caracteres')
    ], description='Cor em formato hexadecimal (ex: #667eea)')
    cor_secundaria = StringField('Cor Secundária', validators=[
        Length(max=7, message='A cor deve ter no máximo 7 caracteres')
    ], description='Cor em formato hexadecimal (ex: #764ba2)')
    
    # Configurações de exibição
    mostrar_contatos = BooleanField('Mostrar Seção de Contatos', default=True)
    mostrar_mapa = BooleanField('Mostrar Mapa do Google', default=True)
    mostrar_redes_sociais = BooleanField('Mostrar Redes Sociais', default=True)
    
    submit = SubmitField('Salvar Configurações') 