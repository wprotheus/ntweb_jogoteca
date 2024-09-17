# Importações necessárias
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length, Email

from jogoteca import db
from jogoteca.models import Game
from jogoteca.models import User


# Formulário para a tabela Usuários
class UsuarioForm(FlaskForm):
    username = StringField('Nome do Usuário', validators=[DataRequired(), Length(min=4, max=17)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=4, max=44)])
    password_again = PasswordField(
        'Confirmar Senha', validators=[
            DataRequired(),
            EqualTo('password', message='As senhas devem ser iguais.')
        ])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=44)])
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', None)

    def validate_username(self, username):
        usuario_existente = User.query.filter_by(username=username.data).first()
        if usuario_existente and usuario_existente.id != self.user_id:
            raise ValidationError("Usuário já cadastrado.")

    def save(self):
        if self.user_id:
            usuario = User.query.get(self.user_id)
            if usuario:
                usuario.username = self.username.data
                usuario.password = self.password.data
                usuario.email = self.email.data
        else:
            usuario = User(
                username=self.username.data,
                password=self.password.data,
                email=self.email.data
            )

        db.session.add(usuario)
        db.session.commit()
        return usuario


# Formulário para a tabela Jogos
class JogoForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    platform = StringField('Plataforma', validators=[DataRequired()])
    category = StringField('Categoria', validators=[DataRequired()])
    description = TextAreaField('Descrição', validators=[DataRequired()])
    rating = StringField('Rating', validators=[DataRequired()])
    price = StringField('Preço', validators=[DataRequired()])
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(JogoForm, self).__init__(*args, **kwargs)
        self.jogo_id = kwargs.get('jogo_id', None)

    def validate_title(self, title):
        jogo_existente = Game.query.filter_by(title=title.data).first()
        if jogo_existente and (self.jogo_id is None or jogo_existente.id != self.jogo_id):
            raise ValidationError("Jogo já cadastrado.")

    def save(self, jogo=None):
        if jogo is None:
            jogo = Game()

        jogo.title = self.title.data
        jogo.platform = self.platform.data
        jogo.category = self.category.data
        jogo.description = self.description.data
        jogo.rating = self.rating.data
        jogo.price = self.price.data

        db.session.add(jogo)
        db.session.commit()
        return jogo
