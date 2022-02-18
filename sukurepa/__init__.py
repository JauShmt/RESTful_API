from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

# DATABASE PARAMS
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ihaveasecret'  # cookies/session variables encryption
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    """ Establish application routes """
    from .api import scraper
    """ Establish application blueprints """
    app.register_blueprint(scraper, url_prefix='/')
    from .models import tablerinho
    create_database(app)
    return app


def create_database(app):
    if not path.exists('G2 API/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')