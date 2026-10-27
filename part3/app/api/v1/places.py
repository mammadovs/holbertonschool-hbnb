#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title', example="Cozy Apartment"),
    'description': fields.String(description='Place description', example="A nice place to stay"),
    'price': fields.Float(required=True, description='Price per night', example=100.0),
    'latitude': fields.Float(required=True, description='Latitude coordinate', example=37.7749),
    'longitude': fields.Float(required=True, description='Longitude coordinate', example=-122.4194)
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Place title', example="Cozy Apartment Updated"),
    'description': fields.String(description='Place description', example="An updated nice place"),
    'price': fields.Float(description='Price per night', example=120.0),
    'latitude': fields.Float(description='Latitude coordinate', example=37.7749),
    'longitude': fields.Float(description='Longitude coordinate', example=-122.4194)
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model, validate=True)
    def post(self):
        """Register a new place for the authenticated user"""
        current_user_id = get_jwt_identity()
        place_data = api.payload
        place_data['owner_id'] = current_user_id

        try:
            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner.id if new_place.owner else None
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f"An error occurred: {str(e)}"}, 400

    def get(self):
        """Retrieve all places (Public endpoint)"""
        places = facade.get_all_places()
        return [{
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'price': p.price,
            'latitude': p.latitude,
            'longitude': p.longitude,
            'owner_id': p.owner.id if p.owner else None
        } for p in places], 200

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        """Get place details by ID (Public endpoint)"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner.id if place.owner else None
        }, 200

    @jwt_required()
    @api.expect(place_update_model, validate=True)
    def put(self, place_id):
        """Update a place (Only the owner or an admin can update it)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if place.owner.id != current_user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        update_data = api.payload
        try:
            updated_place = facade.update_place(place_id, update_data)
            return {'message': 'Place updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f"An error occurred: {str(e)}"}, 400
