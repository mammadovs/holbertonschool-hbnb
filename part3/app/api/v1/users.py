#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, example="John"),
    'last_name': fields.String(required=True, example="Doe"),
    'email': fields.String(required=True, example="john@example.com")
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        user_data = api.payload
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'email': new_user.email}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        users = facade.get_all_users()
        return [{'id': u.id, 'first_name': u.first_name, 'email': u.email} for u in users], 200
