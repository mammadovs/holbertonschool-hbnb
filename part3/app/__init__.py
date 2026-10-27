#!/usr/bin/python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import config

db = SQLAlchemy()
jwt = JWTManager()

# Инициализируем фасад после создания db, чтобы модели могли безопасно его импортировать
from app.services.facade import HBnBFacade
facade = HBnBFacade()

def create_app(config_name='development'):
    """Application factory pattern implementation."""
    app = Flask(__name__)
    
    # Load configuration from the config dictionary
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Create database tables
    with app.app_context():
        from app.models.user import User
        db.create_all()

    # Register API blueprint
    from app.api.v1 import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    return app
