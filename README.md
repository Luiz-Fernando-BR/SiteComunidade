# SiteComunidade
esse projeto se refere a criação de uma comunidade de debates utilizando **Flask**, **Bootsrap** e **Python**.

### Este `README.md` inclui:
1. **Introdução ao projeto**: Explica o objetivo da aplicação e as funcionalidades principais.
2. **Tecnologias utilizadas**: Descreve as principais bibliotecas e ferramentas usadas no projeto.
3. **Estrutura do código**: Detalha a organização do projeto, incluindo explicações sobre as pastas e arquivos principais.
4. **Instruções de execução local**: Passo a passo para rodar a aplicação no ambiente local.

# Comunidade Impressionadora

Este projeto é uma aplicação web desenvolvida com **Flask**, **SQLAlchemy** e outras tecnologias, que visa proporcionar uma plataforma para interação entre usuários, onde eles podem criar contas, fazer login, interagir através de postagens e gerenciar seus perfis. A aplicação é uma rede social simplificada focada no compartilhamento de conhecimento em áreas específicas como **Python**, **SQL**, **Power BI**, **Excel**, entre outras.

## Funcionalidades

A aplicação permite que os usuários:

- **Cadastro e Login**: Os usuários podem criar contas, fazer login e manter uma sessão ativa com a opção de lembrar dados de acesso.
- **Gerenciamento de Perfil**: O usuário pode editar seu perfil, atualizar a foto de perfil e selecionar cursos que deseja compartilhar com outros.
- **Postagens**: Criar, editar e excluir postagens de texto, permitindo que compartilhem ideias e conhecimentos.
- **Interação com Outros Usuários**: Visualizar perfis de outros usuários, visualizar suas postagens e interagir com o conteúdo publicado.

## Tecnologias Utilizadas

Abaixo estão as principais tecnologias utilizadas para desenvolver este projeto:

- **Flask**: Framework principal para o desenvolvimento da aplicação web.
- **Flask-SQLAlchemy**: ORM para interação com o banco de dados.
- **Flask-Bcrypt**: Para criptografia e segurança das senhas dos usuários.
- **Flask-Login**: Para gerenciar sessões de usuário e autenticação.
- **Flask-WTF**: Para facilitar a criação e validação de formulários.
- **Gunicorn**: Servidor WSGI para rodar a aplicação em ambiente de produção.
- **Pillow**: Biblioteca para manipulação e redimensionamento de imagens, usada para fotos de perfil.

## Estrutura do Projeto

A estrutura do projeto está organizada da seguinte forma:

### Descrição dos Arquivos

1. **`app/__init__.py`**: Arquivo responsável por inicializar o Flask, configurar a aplicação, a conexão com o banco de dados, entre outras configurações iniciais.
2. **`app/models.py`**: Define os modelos de dados da aplicação, como o modelo `Usuario` (para gerenciar usuários) e `Post` (para gerenciar postagens).
3. **`app/routes.py`**: Contém as rotas da aplicação, ou seja, os endpoints responsáveis por processar as requisições HTTP e renderizar as respostas (exemplo: criação de posts, login, exibição de perfis).
4. **`app/forms.py`**: Contém os formulários utilizados para criar contas, editar perfis, fazer login, etc. Usa a biblioteca **WTForms** para validação e controle de dados dos formulários.
5. **`app/templates/`**: Contém os templates HTML utilizados pelo Flask, como páginas de login, perfil, home, etc.
6. **`app/static/`**: Contém arquivos estáticos (imagens, arquivos CSS, JavaScript) que são servidos pela aplicação. Exemplos incluem fotos de perfil dos usuários.
7. **`main.py`**: Arquivo responsável por iniciar a aplicação quando executado localmente ou em produção.
8. **`Procfile`**: Arquivo utilizado pelo Heroku para iniciar a aplicação em ambiente de produção. Contém o comando para rodar o servidor **Gunicorn**.
9. **`requirements.txt`**: Contém todas as dependências necessárias para o funcionamento da aplicação, incluindo Flask, Gunicorn, Flask-SQLAlchemy, etc.

## Como Rodar a Aplicação Localmente

### Pré-requisitos

- Python 3.8 ou superior
- `pip` (gerenciador de pacotes do Python)

### Passos para execução

1. Clone o repositório:
   ```bash
   git clone https://github.com/usuario/comunidadeimpressionadora.git
   cd comunidadeimpressionadora
   
2. Crie e ative um ambiente virtual:
python -m venv venv
source venv/bin/activate  # No Windows use venv\Scripts\activate

3. Instalar as dependências:
   pip install -r requirements.txt

4. Configurar o banco de dados:
   O projeto usa SQLite por padrão, mas pode ser configurado para outros bancos (como MySQL ou PostgreSQL) ajustando o arquivo config.py.
   Inicialize o banco de dados com:
   flask db upgrade
5. Rode uma aplicação localmente:
   python main.py 
