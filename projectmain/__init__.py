from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from projectmain.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'Main.mlogin'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	
	db.init_app(app) 
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)
	
	from projectmain.main.routs import Main
	from projectmain.admin.routs import Admin
	from projectmain.agent.routs import Agent
	from projectmain.consumer.routs import Consumer
	from projectmain.errors.handlers import Errors
	app.register_blueprint(Main)
	app.register_blueprint(Admin)
	app.register_blueprint(Agent)
	app.register_blueprint(Consumer)
	app.register_blueprint(Errors)
	return app