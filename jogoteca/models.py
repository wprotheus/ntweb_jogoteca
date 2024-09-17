from datetime import datetime

from jogoteca import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    username = db.Column(db.String(17), unique=True, nullable=False)
    password = db.Column(db.String(44), nullable=False)
    email = db.Column(db.String(44), nullable=False)

    def __repr__(self):
        return f'<User {self.usuario}>'


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(26), unique=True, nullable=False)
    platform = db.Column(db.String(17), nullable=False)
    category = db.Column(db.String(17), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Float(8), nullable=False)

    def __repr__(self):
        return f'<Game {self.titulo}>'
