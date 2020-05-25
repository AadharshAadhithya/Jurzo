from flask import *

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager





jurzo = Flask(__name__)
jurzo.config['SECRET_KEY']='fd1690f36c025ca204c6fececc84db4d'
jurzo.config['SQLALCHEMY_DATABASE_URI']='sqlite:///jurzo.db'
db=SQLAlchemy(jurzo)
bcrypt=Bcrypt(jurzo)
login_manager= LoginManager(jurzo)
login_manager.login_view='login'

from Jurzo import routes


