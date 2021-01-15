from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Flask Application Object
app = Flask(__name__)
app.config['SECRET_KEY'] = '4940a9c6b8335931fded4f3795edab28'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/diet.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database Connection and object of SQLAlchemy
db = SQLAlchemy(app)

# LoginManager instance and login parameters
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Proszę się zalogować aby uzyskać dostęp do tej strony.'

from dietapp import routes
