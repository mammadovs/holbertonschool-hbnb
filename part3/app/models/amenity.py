#!/usr/bin/python3
from app.models.base_model import BaseModel
from app import db

class Amenity(BaseModel):
    """Amenity representation class with SQLAlchemy mapping."""
    
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name

