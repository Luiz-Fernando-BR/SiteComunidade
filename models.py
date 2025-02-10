from comunidadeimpressionadora import database, login_manager
from datetime import datetime
from flask_login import UserMixin

# Função para carregar um usuário pelo ID (necessário para Flask-Login)
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

# Modelo de usuário, representando cada membro da comunidade
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)  # Identificador único do usuário
    username = database.Column(database.String(50), nullable=False)  # Nome de usuário (máx. 50 caracteres)
    email = database.Column(database.String(150), nullable=False, unique=True)  # E-mail único (máx. 150 caracteres)
    senha = database.Column(database.String(200), nullable=False)  # Senha criptografada
    foto_perfil = database.Column(database.String, default='default.jpg')  # Nome do arquivo da foto de perfil
    posts = database.relationship('Post', backref='autor', lazy=True)  # Relacionamento com os posts do usuário
    cursos = database.Column(database.String, nullable=False, default='Não Informado')  # Cursos cadastrados pelo usuário

    # Método para contar o número de posts do usuário
    def contar_posts(self):
        return len(self.posts)

# Modelo de post, representando as publicações feitas pelos usuários
class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)  # Identificador único do post
    titulo = database.Column(database.String, nullable=False)  # Título do post
    corpo = database.Column(database.Text, nullable=False)  # Conteúdo do post
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)  # Data de criação do post
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)  # ID do autor do post (chave estrangeira)
