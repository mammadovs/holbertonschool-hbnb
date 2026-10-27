#!/usr/bin/python3
from app.models.base_model import BaseModel
from app import db

class Place(BaseModel):
    """Place representation class with SQLAlchemy mapping."""
    
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, description, price, latitude, longitude, owner_id=None, **kwargs):
        super().__init__(**kwargs)
        self.validate(title, price, latitude, longitude)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        if owner_id:
            self.owner_id = owner_id

    @staticmethod
    def validate(title, price, latitude, longitude):
        if not title or not title.strip():
            raise ValueError("Title is required")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number")
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

