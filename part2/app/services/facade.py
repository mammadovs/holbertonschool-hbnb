#!/usr/bin/python3
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    """Facade class to manage communication between layers"""
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # --- User Methods ---
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)

    # --- Amenity Methods ---
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)

    # --- Place Methods ---
    def create_place(self, place_data):
        """Creates a place and links owner and amenities"""
        owner_id = place_data.pop('owner_id', None)
        amenity_ids = place_data.pop('amenities', [])
        
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Owner not found")
            
        place = Place(**place_data, owner=owner)
        
        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if amenity:
                place.add_amenity(amenity)
                
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        return self.place_repo.update(place_id, place_data)

    # --- Review Methods ---
    def create_review(self, review_data):
        """Creates a review linked to a user and a place"""
        user_id = review_data.pop('user_id', None)
        place_id = review_data.pop('place_id', None)
        
        user = self.get_user(user_id)
        place = self.get_place(place_id)
        
        if not user or not place:
            raise ValueError("User or Place not found")
            
        review = Review(**review_data, user=user, place=place)
        self.review_repo.add(review)
        place.add_review(review) # Link review to the place object
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()
