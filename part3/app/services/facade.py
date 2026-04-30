#!/usr/bin/python3
from app.models.user import User
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Creates a new user and hashes the password via the User model."""
        user = User(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email'),
            password=user_data.get('password'),
            is_admin=user_data.get('is_admin', False)
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieves a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieves a user by email address."""
        # This method is required to check for duplicate emails in the API
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieves all registered users."""
        return self.user_repo.get_all()
