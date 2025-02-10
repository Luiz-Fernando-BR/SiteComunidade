from flask import render_template, redirect, url_for, flash, request, abort
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

# Rota para a página inicial
@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())  # Obtém os posts ordenados por ID de forma decrescente
    return render_template('home.html', posts=posts)

# Rota para a página de contato
@app.route('/contato')
def contato():
    return render_template('contato.html')

# Rota para listar usuários (apenas para usuários autenticados)
@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

# Rota para login e criação de conta
@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    
    # Processo de login
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            return redirect(par_next) if par_next else redirect(url_for('home'))
        else:
            flash(f'Falha no Login. E-mail ou Senha Incorretos', 'alert-danger')
    
    # Processo de criação de conta
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode("utf-8")
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

# Rota para logout
@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout Feito com Sucesso', 'alert-success')
    return redirect(url_for('home'))

# Rota para exibir perfil do usuário
@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)

# Rota para criação de post
@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)

# Função auxiliar para salvar imagens de perfil
def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)  # Gera um nome único
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

# Rota para edição de perfil
@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        database.session.commit()
        flash('Perfil atualizado com Sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)

# Rota para exibição de post específico
@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = FormCriarPost() if current_user == post.autor else None
    if form and request.method == 'GET':
        form.titulo.data = post.titulo
        form.corpo.data = post.corpo
    elif form and form.validate_on_submit():
        post.titulo = form.titulo.data
        post.corpo = form.corpo.data
        database.session.commit()
        flash('Post Atualizado com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('post.html', post=post, form=form)

# Rota para exclusão de post
@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluído com Sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)  # Retorna erro 403 caso o usuário não tenha permissão
