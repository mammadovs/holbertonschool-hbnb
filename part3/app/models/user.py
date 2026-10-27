#!/usr/bin/python3
from app.models.base_model import BaseModel
from flask_bcrypt import Bcrypt
from app import db

bcrypt = Bcrypt()

class User(BaseModel):
    """User representation class with SQLAlchemy mapping and relationships."""
    
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False, **kwargs):
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.hash_password(password)

    def hash_password(self, password):
        """Hashes the password using Bcrypt."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies the password against the hashed version."""
        return bcrypt.check_password_hash(self.password, password)

