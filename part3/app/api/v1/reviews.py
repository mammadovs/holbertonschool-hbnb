#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)', min=1, max=5),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    def post(self):
        """Create a new review"""
        try:
            new_review = facade.create_review(api.payload)
            return {'id': new_review.id, 'text': new_review.text}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        return [{'id': r.id, 'text': r.text, 'rating': r.rating} for r in reviews], 200
