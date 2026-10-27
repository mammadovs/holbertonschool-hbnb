#!/usr/bin/python3
from app.models.base_model import BaseModel
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(BaseModel):
    """User representation class with password hashing support."""
    
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = self.hash_password(password)

    def hash_password(self, password):
        """Hash the user password using bcrypt."""
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the provided password against the stored hash."""
        return bcrypt.check_password_hash(self.password, password)

