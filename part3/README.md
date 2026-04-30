## Testing and Validation

I have performed thorough testing and validation of the HBnB API to ensure all business logic and endpoints function as expected.

### 1. User Endpoints
- **Operations:** Verified User creation, listing, and updates.
- **Validation:** Confirmed that the system correctly blocks duplicate emails (Returns `400 Bad Request`).
- **Data Integrity:** Ensured UUIDs and timestamps are automatically generated.

### 2. Amenities
- **Operations:** Successfully tested creation and retrieval of amenities.
- **Consistency:** Each amenity is correctly stored and can be linked to multiple places.

### 3. Place Logic & Relationships
- **Linking:** Verified that every Place is correctly associated with an owner (User) and specific Amenities.
- **Serialization:** Confirmed that fetching a Place returns nested details about the owner and the amenities list.

### 4. Review System
- **Business Rules:** Enforced rating validation. Tested that ratings must be between **1 and 5**.
- **Edge Cases:** Verified that reviews cannot be created without a valid `user_id` and `place_id`.

### 5. API Documentation & Manual Testing
- **Swagger UI:** Automatically generated documentation is accessible at the root URL.
- **Tools Used:** All endpoints were validated using **cURL** and **Postman** to ensure correct HTTP status codes (201 for creation, 400 for bad data, 404 for missing resources).

### How to Run Tests
To execute the automated unit tests, run:
```bash
python3 -m unittest discover tests
```
