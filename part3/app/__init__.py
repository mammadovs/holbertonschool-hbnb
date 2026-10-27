#!/usr/bin/python3
from flask import Flask
from app.config import config

def create_app(config_name='development'):
    """Application factory pattern implementation."""
    app = Flask(__name__)
    
    # Load configuration from the config dictionary
    app.config.from_object(config[config_name])

    # Register blueprints and initialize extensions here in later tasks
    # Example:
    # from app.api.v1 import api_bp
    # app.register_blueprint(api_bp, url_prefix='/api/v1')

    return app

