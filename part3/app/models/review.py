#!/usr/bin/python3
from app.models.base_model import BaseModel
from app import db

class Review(BaseModel):
    """Review class that inherits from BaseModel with SQLAlchemy relationships."""
    
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # SQLAlchemy relationships
    user = db.relationship('User', backref=db.backref('reviews_written', lazy=True))

    def __init__(self, text, rating, place_id, user_id, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

