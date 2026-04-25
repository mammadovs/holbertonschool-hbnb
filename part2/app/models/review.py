#!/usr/bin/python3
from .base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place  # Объект Place
        self.user = user    # Объект User
