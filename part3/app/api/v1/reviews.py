#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import facade

api = Namespace('reviews', description='Review operations')

# Модель для создания отзыва (user_id больше не требуется от клиента, он берется из JWT)
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review', example="Great place!"),
    'rating': fields.Integer(required=True, description='Rating (1-5)', min=1, max=5, example=5),
    'place_id': fields.String(required=True, description='ID of the place', example="uuid-of-place")
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Text of the review', example="Updated review text"),
    'rating': fields.Integer(description='Rating (1-5)', min=1, max=5, example=4)
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model, validate=True)
    def post(self):
        """Create a new review (Authenticated user)"""
        current_user_id = get_jwt_identity()
        review_data = api.payload
        review_data['user_id'] = current_user_id

        place_id = review_data.get('place_id')
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Проверка: нельзя оставлять отзыв на собственное место
        if place.owner and place.owner.id == current_user_id:
            return {'error': 'You cannot review your own place'}, 400

        # Проверка: нельзя оставлять повторный отзыв на одно и то же место
        existing_reviews = facade.get_all_reviews()
        for r in existing_reviews:
            if r.place.id == place_id and r.user.id == current_user_id:
                return {'error': 'You have already reviewed this place'}, 400

        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id if new_review.user else None,
                'place_id': new_review.place.id if new_review.place else None
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f"An error occurred: {str(e)}"}, 400

    def get(self):
        """Retrieve all reviews (Public endpoint)"""
        reviews = facade.get_all_reviews()
        return [{
            'id': r.id,
            'text': r.text,
            'rating': r.rating,
            'user_id': r.user.id if r.user else None,
            'place_id': r.place.id if r.place else None
        } for r in reviews], 200

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        """Get review details by ID (Public endpoint)"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id if review.user else None,
            'place_id': review.place.id if review.place else None
        }, 200

    @jwt_required()
    @api.expect(review_update_model, validate=True)
    def put(self, review_id):
        """Update a review (Only the author can update it)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if review.user.id != current_user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        update_data = api.payload
        try:
            updated_review = facade.update_review(review_id, update_data)
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f"An error occurred: {str(e)}"}, 400

    @jwt_required()
    def delete(self, review_id):
        """Delete a review (Only the author or admin can delete it)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if review.user.id != current_user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except Exception as e:
            return {'error': f"An error occurred: {str(e)}"}, 400

