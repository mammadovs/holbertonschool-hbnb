#!/usr/bin/python3
from .base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.validate(title, price, latitude, longitude)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.amenities = []
        self.reviews = []

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
