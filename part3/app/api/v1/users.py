#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user', example="John"),
    'last_name': fields.String(required=True, description='Last name of the user', example="Doe"),
    'email': fields.String(required=True, description='Email of the user', example="john@example.com"),
    'password': fields.String(required=True, description='Password of the user', example="secretpassword")
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user', example="JohnUpdated"),
    'last_name': fields.String(description='Last name of the user', example="DoeUpdated")
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        """Register a new user (password is securely hashed)"""
        user_data = api.payload
        
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
            return {'error': str(e)}, 400

    def get(self):
        """Retrieve all users (passwords/hashes are strictly excluded)"""
        users = facade.get_all_users()
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
            
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()
    @api.expect(user_update_model, validate=True)
    def put(self, user_id):
        """Update user profile (Only the user themselves or an admin can update it)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        # Проверка прав: пользователь может менять только свой профиль, либо должен быть админом
        if user_id != current_user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        update_data = api.payload
        try:
            updated_user = facade.update_user(user_id, update_data)
            return {
                'message': 'User updated successfully',
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f"An error occurred: {str(e)}"}, 400

