#!/usr/bin/python3
from .base_model import BaseModel

class Review(BaseModel):
    """Review class that inherits from BaseModel"""
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text        # The content of the review
        self.rating = rating    # Integer between 1 and 5
        self.place = place      # The Place object being reviewed
        self.user = user        # The User object who wrote the review
