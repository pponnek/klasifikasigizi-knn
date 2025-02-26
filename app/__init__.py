import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    CORS(app)

    from app.routes.authRoutes import auth_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')

    logging.basicConfig(level=logging.INFO)
    logging.info('App started')


    return app

from app.models import user