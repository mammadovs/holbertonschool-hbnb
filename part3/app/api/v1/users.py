#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app import facade

api = Namespace('users', description='User operations')

# User model definition for documentation and input validation (includes password)
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user', example="John"),
    'last_name': fields.String(required=True, description='Last name of the user', example="Doe"),
    'email': fields.String(required=True, description='Email of the user', example="john@example.com"),
    'password': fields.String(required=True, description='Password of the user', example="secretpassword")
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        """Register a new user (password is securely hashed)"""
        user_data = api.payload
        
        # Check if email is already registered
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400
            
        try:
            # Create user (facade/model handles password hashing automatically)
            new_user = facade.create_user(user_data)
            
            # Return created user info strictly without the password/hash
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        """Retrieve all users (passwords/hashes are strictly excluded)"""
        users = facade.get_all_users()
        
        # Return users list ensuring passwords are never exposed in GET requests
        return [{
            'id': u.id,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email
        } for u in users], 200

@api.route('/<string:user_id>')
class UserResource(Resource):
    def get(self, user_id):
        """Get user by ID (password/hash is strictly excluded)"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
            
        # Return single user info strictly without the password/hash
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

