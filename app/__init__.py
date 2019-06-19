# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(env_config):
	app = Flask(__name__, instance_relative_config=True)

	app.config.from_object(app_config[env_config])
	app.config.from_pyfile('config.py')
	
	db.init_app(app)
	login_manager.init_app(app)
	login_manager.login_message = "You must be logged in to access this page."
	login_manager.login_view = "auth.login"
	
	Bootstrap(app)	
	migrate = Migrate(app, db)

	from app import models

	from .admin import admin as admin_blueprint
	app.register_blueprint(admin_blueprint, url_prefix='/admin')

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .home import home as home_blueprint
	app.register_blueprint(home_blueprint)

	return app