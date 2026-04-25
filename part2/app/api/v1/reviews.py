#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app import facade

api = Namespace('reviews', description='Review operations')

# Review model for validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
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
            return {'id': new_review.id, 'text': new_review.text, 'rating': new_review.rating}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        return [{'id': r.id, 'text': r.text, 'rating': r.rating} for r in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user': {'id': review.user.id, 'first_name': review.user.first_name},
            'place': {'id': review.place.id, 'title': review.place.title}
        }, 200
