#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, example="John"),
    'last_name': fields.String(required=True, example="Doe"),
    'email': fields.String(required=True, example="john.doe@example.com")
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        """Register a new user with email validation"""
        user_data = api.payload
        
        # Check if email is already taken
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except ValueError as e:
            # Return specific validation error (e.g., "Invalid email format")
            return {'error': str(e)}, 400
