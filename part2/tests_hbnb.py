#!/usr/bin/python3
import unittest
from app import create_app

class TestHBNB(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_user_creation(self):
        """Test valid user creation"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_invalid_user_creation(self):
        """Test user creation with missing email (Validation check)"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test"
        })
        self.assertEqual(response.status_code, 400)

    def test_amenity_creation(self):
        """Test amenity creation"""
        response = self.client.post('/api/v1/amenities/', json={"name": "WiFi"})
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
