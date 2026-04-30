#!/usr/bin/python3
import unittest
from app import create_app

class TestHBNB(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_invalid_rating(self):
        """Test review creation with rating 6 (Should fail)"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Too good",
            "rating": 6,
            "user_id": "any",
            "place_id": "any"
        })
        self.assertEqual(response.status_code, 400)

    def test_duplicate_email(self):
        """Test duplicate email validation"""
        payload = {"first_name": "A", "last_name": "B", "email": "test@test.com"}
        self.client.post('/api/v1/users/', json=payload)
        response = self.client.post('/api/v1/users/', json=payload)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
