from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from Jurzo.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
mail = Mail()


def create_app(config_class=Config):
    jurzo = Flask(__name__)
    jurzo.config.from_object(Config)
    db.init_app(jurzo)
    bcrypt.init_app(jurzo)
    login_manager.init_app(jurzo)
    mail.init_app(jurzo)
    from Jurzo.users.routes import users
    from Jurzo.pages.routes import pages
    from Jurzo.main.routes import main
    jurzo.register_blueprint(users)
    jurzo.register_blueprint(pages)
    jurzo.register_blueprint(main)

    return jurzo
