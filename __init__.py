# Importando as bibliotecas necessárias para o funcionamento da aplicação
from flask import Flask  # Flask para criar a aplicação web
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy para gerenciar o banco de dados ORM
import os  # Biblioteca para manipulação de caminhos de arquivos do sistema operacional
from flask_bcrypt import Bcrypt  # Bcrypt para criptografar senhas de forma segura
from flask_login import LoginManager  # LoginManager para gerenciar autenticação e sessões de usuários
import sqlalchemy  # SQLAlchemy puro para inspecionar o banco de dados

# Inicializando a aplicação Flask
app = Flask(__name__)

# Definição de uma chave secreta para segurança da aplicação.
# Essa chave é usada para proteger sessões, cookies e CSRF (Cross-Site Request Forgery).
app.config['SECRET_KEY'] = '29cecf8afd6176f06bb3f55472d490d1'

# Configuração do banco de dados:
# Se houver uma variável de ambiente DATABASE_URL (usada em deploys como Heroku), utilizamos essa configuração.
if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    # Obtendo o diretório absoluto onde o script está localizado
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    # Configurando o banco de dados SQLite, garantindo que ele seja salvo no mesmo diretório da aplicação
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "comunidade.db")}'

# Inicializando o objeto SQLAlchemy, que será responsável pela comunicação e manipulação do banco de dados
database = SQLAlchemy(app)

# Inicializando o Bcrypt para possibilitar a criptografia de senhas dos usuários
bcrypt = Bcrypt(app)

# Inicializando o LoginManager para gerenciar o login e a autenticação de usuários
login_manager = LoginManager(app)

# Definindo a página de login padrão para usuários não autenticados
login_manager.login_view = 'login'

# Configuração da categoria da mensagem flash ao redirecionar usuários não autenticados
login_manager.login_message_category = 'alert-info'

# Importando os modelos para garantir que as tabelas sejam reconhecidas pelo SQLAlchemy
from comunidadeimpressionadora import models

# Criando um mecanismo de inspeção do banco de dados para verificar a existência da tabela "usuario"
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)

# Caso a tabela "usuario" não exista, o banco de dados será recriado
if not inspector.has_table("usuario"):
    with app.app_context():
        database.drop_all()  # Remove todas as tabelas existentes (caso necessário)
        database.create_all()  # Cria as tabelas novamente
        print("Base de dados criada com sucesso")  # Mensagem para indicar que a base foi criada
else:
    print("Base de dados já existente")  # Caso a base já exista, nenhuma ação é tomada

# Importando o arquivo de rotas, que contém as definições de URLs e lógica da aplicação
# Esse import deve ser feito no final para evitar importações circulares
from comunidadeimpressionadora import routes
