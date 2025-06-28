from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Entrar')

class ExameForm(FlaskForm):
    nome = StringField('Nome do Exame', validators=[DataRequired(), Length(min=3, max=100)])
    descricao = TextAreaField('Descrição', validators=[DataRequired(), Length(min=10, max=500)])
    preparo = TextAreaField('Preparo Necessário', validators=[DataRequired(), Length(min=5, max=300)])
    documentos = TextAreaField('Documentos Exigidos', validators=[DataRequired(), Length(min=5, max=200)])
    pos_exame = TextAreaField('Cuidados Após o Exame', validators=[DataRequired(), Length(min=5, max=300)])
    tempo = StringField('Duração', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Salvar Exame')

class UploadExcelForm(FlaskForm):
    arquivo = FileField('Arquivo Excel', validators=[
        FileRequired(),
        FileAllowed(['xlsx', 'xls'], 'Apenas arquivos Excel (.xlsx, .xls) são permitidos!')
    ])
    submit = SubmitField('Importar Exames') 