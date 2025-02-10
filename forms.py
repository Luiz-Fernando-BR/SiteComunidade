from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user

# Formulário para criar uma nova conta de usuário
class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])  # Campo para o nome de usuário
    email = StringField('E-mail', validators=[DataRequired(), Email()])  # Campo para o e-mail
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])  # Campo para senha
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])  # Confirmação de senha
    botao_submit_criarconta = SubmitField('Criar Conta')  # Botão de submissão

    # Validação para verificar se o e-mail já está cadastrado
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar')

# Formulário para login de usuário
class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])  # Campo para o e-mail
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])  # Campo para senha
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')  # Opção para lembrar login
    botao_submit_login = SubmitField('Fazer Login')  # Botão de submissão

# Formulário para edição do perfil do usuário
class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])  # Campo para nome de usuário
    email = StringField('E-mail', validators=[DataRequired(), Email()])  # Campo para e-mail
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])  # Campo para upload de foto de perfil
    
    # Checkboxes para cursos selecionáveis pelo usuário
    curso_excel = BooleanField('Excel')
    curso_vba = BooleanField('VBA')
    curso_powerbi = BooleanField('Power BI')
    curso_python = BooleanField('Python')
    curso_ppt = BooleanField('Apresentações')
    curso_sql = BooleanField('SQL')
    
    botao_submit_editarperfil = SubmitField('Confirmar Edição')  # Botão de submissão

    # Validação para verificar se o e-mail já existe no banco de dados
    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse e-mail. Cadastre outro e-mail')

# Formulário para criação de postagens
class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2, 140)])  # Campo para título da postagem
    corpo = TextAreaField('Escreva seu Post Aqui', validators=[DataRequired()])  # Campo para conteúdo do post
    botao_submit = SubmitField('Criar Post')  # Botão de submissão
