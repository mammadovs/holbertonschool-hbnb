#!/usr/bin/python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import config

db = SQLAlchemy()
jwt = JWTManager()

from app.services.facade import HBnBFacade
facade = HBnBFacade()

def create_app(config_name='development'):
    """Application factory pattern implementation."""
    app = Flask(__name__)
    
    app.config.from_object(config[config_name])
    
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    
    # Create tables for all models
    with app.app_context():
        from app.models.user import User
        from app.models.amenity import Amenity
        from app.models.place import Place
        from app.models.review import Review
        db.create_all()

    from app.api.v1 import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    return app

