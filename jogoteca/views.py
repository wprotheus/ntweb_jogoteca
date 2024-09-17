# Importações necessárias
from flask import render_template, redirect, url_for, request

from jogoteca import app, db
from jogoteca import forms
from jogoteca.forms import JogoForm
from jogoteca.models import User, Game


## Endpoints da aplicação

# Página inicial
@app.route('/')
def home():
    return render_template('home.html')


## Endpoins para Usuários


# Listagem dos usuários
@app.route('/usuario/lista', methods=['GET'])
def listaUsuarios():
    usuarios = User.query.order_by(User.username.desc()).all()
    return render_template('/usuarios/lista_usuarios.html', usuarios=usuarios)


# Cadastro de novos usuarios
@app.route('/usuario/cadastro', methods=['GET', 'POST'])
def cadastroUsuario():
    form = forms.UsuarioForm()
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('listaUsuarios'))

    return render_template('/usuarios/cadastro_usuario.html', form=form)


# Buscar Usuário por ID e Atualizar
@app.route('/usuario/<int:id>', methods=['GET', 'POST'])
def editaAtualizaUsuario(id):
    usuario = User.query.get_or_404(id)
    form = forms.UsuarioForm(obj=usuario, user_id=id)  # Passa o ID do usuário ao formulário

    if form.validate_on_submit():
        form.save()  # Não é necessário passar o objeto usuario, o método save deve lidar com isso
        return redirect(url_for('listaUsuarios'))

    return render_template('/usuarios/edita_usuario.html', form=form)


# Deletar Usuário por ID
@app.route('/usuario/deletar/<int:id>', methods=['POST'])
def deletarUsuarioId(id):
    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('listaUsuarios'))


# Buscar Usuário por Username
@app.route('/usuario/buscar', methods=['GET'])
def buscarUsuarioPorNome():
    usuario = request.args.get('usuario')
    if usuario:
        user = User.query.filter(User.username.ilike(f'%{usuario}%')).all()  # ilike -> case-insensitive
        return render_template('usuarios/lista_usuarios.html', usuarios=user)
    return redirect(url_for('listaUsuarios'))


# Listagem dos jogos
@app.route('/jogo/lista', methods=['GET'])
def listaJogos():
    jogos = Game.query.order_by(Game.title.asc()).all()
    return render_template('/jogos/lista_jogos.html', jogos=jogos)


# Cadastro de novos jogos
@app.route('/jogo/cadastro', methods=['GET', 'POST'])
def cadastroJogo():
    form = forms.JogoForm()
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('listaJogos'))
    return render_template('/jogos/cadastro_jogo.html', form=form)


# Editar Jogo por ID e Atualizar
@app.route('/jogo/<int:id>', methods=['GET', 'POST'])
def editaAtualizaJogo(id):
    jogo = Game.query.get_or_404(id)
    form = JogoForm(obj=jogo, jogo_id=id)  # Passa o ID do jogo ao formulário

    if form.validate_on_submit():
        form.save(jogo)
        return redirect(url_for('listaJogos'))

    return render_template('/jogos/edita_jogo.html', form=form, jogo=jogo)


# Deletar Jogo por ID
@app.route('/jogo/deletar/<int:id>', methods=['POST'])
def deletarJogoId(id):
    jogo = Game.query.get_or_404(id)
    db.session.delete(jogo)
    db.session.commit()
    return redirect(url_for('listaJogos'))


# Buscar Jogo por Title
@app.route('/jogo/buscar', methods=['GET'])
def buscarJogoPorTitle():
    title = request.args.get('title')
    if title:
        jogo = Game.query.filter(Game.title.ilike(f'%{title}%')).all()  # ilike -> case-insensitive
        return render_template('/jogos/lista_jogos.html', jogos=jogo)
    return redirect(url_for('listaJogos'))
