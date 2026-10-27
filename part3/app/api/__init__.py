#!/usr/bin/python3
from flask import Flask
from app.config import config
from app.services.facade import HBnBFacade

facade = HBnBFacade()

def create_app(config_name='development'):
    """Application factory pattern implementation."""
    app = Flask(__name__)
    
    # Load configuration from the config dictionary
    app.config.from_object(config[config_name])

    # Register API blueprint
    from app.api.v1 import api_bp
    app.register_blueprint(api_bp)

    return app

