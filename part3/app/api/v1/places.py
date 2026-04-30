#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, example="Cozy Apartment"),
    'description': fields.String(example="A nice place to stay"),
    'price': fields.Float(required=True, example=100.0),
    'latitude': fields.Float(required=True, example=37.7749),
    'longitude': fields.Float(required=True, example=-122.4194),
    'owner_id': fields.String(required=True, example="user-uuid-here")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    def post(self):
        """Register a new place"""
        place_data = api.payload
        try:
            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'price': new_place.price
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f"An error occurred: {str(e)}"}, 400

    def get(self):
        """Retrieve all places"""
        places = facade.get_all_places()
        return [{'id': p.id, 'title': p.title, 'price': p.price} for p in places], 200
