#!/usr/bin/python3
from app.models.base_model import BaseModel
from app import db

# Ассоциативная таблица для связи Many-to-Many между Place и Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """Place representation class with SQLAlchemy relationships."""
    
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # SQLAlchemy relationships
    owner = db.relationship('User', backref=db.backref('places_owned', lazy=True))
    reviews = db.relationship('Review', backref='place', cascade='all, delete-orphan', lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery',
                                backref=db.backref('places', lazy=True))

    def __init__(self, title, description, price, latitude, longitude, owner_id, **kwargs):
        super().__init__(**kwargs)
        self.validate(title, price, latitude, longitude)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
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

