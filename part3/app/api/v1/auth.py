#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app import facade

api = Namespace('auth', description='Authentication operations')

auth_model = api.model('Auth', {
    'email': fields.String(required=True, description='User email', example='alice@example.com'),
    'password': fields.String(required=True, description='User password', example='supersecretpassword')
})

@api.route('/login')
class Login(Resource):
    @api.expect(auth_model, validate=True)
    def post(self):
        """Authenticate user and return a JWT access token"""
        credentials = api.payload
        email = credentials.get('email')
        password = credentials.get('password')

        # Find user by email
        user = facade.get_user_by_email(email)
        
        # Verify user existence and password correctness
        if not user or not user.verify_password(password):
            return {'error': 'Invalid email or password'}, 401

        # Generate JWT access token with additional claims
        additional_claims = {'is_admin': getattr(user, 'is_admin', False)}
        access_token = create_access_token(identity=user.id, additional_claims=additional_claims)

        return {'access_token': access_token}, 200

