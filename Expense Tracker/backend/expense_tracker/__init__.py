from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from .constants import *

db = SQLAlchemy()
jwt = JWTManager()

def _read_from_env(key):
    return os.environ.get(key)

def create_tables(app):
    with app.app_context():
        db.create_all()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = _read_from_env(SECRET_KEY)
    
    jwt.init_app(app)

    from .auth import auth
    from .expense import expense
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(expense, url_prefix='/expenses')
    
    DB_URL = _read_from_env(MYSQL_DB_URL)
    DBNAME = _read_from_env(DB_NAME)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_URL}/{DBNAME}'
    db.init_app(app)

    from .models import User, Expense
    create_tables(app)


    return app