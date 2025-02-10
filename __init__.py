# Importando as bibliotecas necessárias para o funcionamento da aplicação
from flask import Flask  # Flask para criar a aplicação web
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy para gerenciar o banco de dados
import os  # Biblioteca para manipulação de caminhos de arquivos
from flask_bcrypt import Bcrypt  # Bcrypt para criptografar senhas de forma segura
from flask_login import LoginManager  # LoginManager para gerenciar autenticação e sessões de usuários

# Inicializando a aplicação Flask
app = Flask(__name__)

# Definindo uma chave secreta para segurança (usada em sessões, cookies e CSRF)
app.config['SECRET_KEY'] = '29cecf8afd6176f06bb3f55472d490d1'
if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
# Definindo o caminho absoluto para o banco de dados, garantindo que o banco de dados esteja no mesmo diretório da aplicação
    base_dir = os.path.abspath(os.path.dirname(__file__))  # Obtém o diretório onde o script está localizado
# Configura o URI do banco de dados SQLite, usando o caminho absoluto para garantir que o banco de dados seja acessado corretamente
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "comunidade.db")}'

# Inicializando o objeto SQLAlchemy, que será responsável pela comunicação com o banco de dados
database = SQLAlchemy(app)

# Inicializando o Bcrypt para criptografia de senhas
bcrypt = Bcrypt(app)

# Inicializando o LoginManager para gerenciar o login e a autenticação de usuários
login_manager = LoginManager(app)
# Definindo qual será a página de login caso o usuário não esteja autenticado
login_manager.login_view = 'login'
# Configurando a categoria da mensagem de alerta quando o usuário não estiver autenticado
login_manager.login_message_category = 'alert-info'

# Importando o arquivo de rotas, que contém as definições de URLs e lógica da aplicação
# Isso é necessário para que as rotas da aplicação sejam carregadas depois que a app foi configurada
from comunidadeimpressionadora import routes
