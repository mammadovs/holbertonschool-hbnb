#!/usr/bin/python3
from flask import Flask
from app.config import config
from app.services.facade import HBnBFacade
from flask_jwt_extended import JWTManager

facade = HBnBFacade()
jwt = JWTManager()

def create_app(config_name='development'):
    """Application factory pattern implementation."""
    app = Flask(__name__)
    
    # Load configuration from the config dictionary
    app.config.from_object(config[config_name])

    # Initialize JWT Manager
    jwt.init_app(app)

    # Register API blueprint
    from app.api.v1 import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    return app

