from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

# App Config.

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'