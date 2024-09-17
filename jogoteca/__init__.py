# Importações necessárias
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from local_settings import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Para usar o Postgresql 'postgresql://usuario:senhaUser@localhost/jogoteca.db
# Configuração Banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jogoteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Instanciando os objetos 'banco de dados' e 'migrate'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importação dos Endpoints
from jogoteca.views import *
from jogoteca.models import *
