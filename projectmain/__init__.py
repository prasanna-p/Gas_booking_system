from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '3aa8894e55eef76b1e94c9fcf3661dfb06f10f69'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gas1db.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from projectmain import routs 
