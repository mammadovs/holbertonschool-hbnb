# HBnB API Testing Report

## 1. Overview
This report documents the validation and testing phase of the HBnB API implementation. Testing was performed using automated unit tests, manual cURL commands, and Swagger documentation.

## 2. Validation Rules Implemented
- **User:** Mandatory fields (first_name, last_name, email). Email uniqueness enforced.
- **Place:** Latitude (-90 to 90), Longitude (-180 to 180), and non-negative price.
- **Review:** Rating must be an integer between 1 and 5.
- **Amenity:** Name is mandatory.

## 3. Test Cases and Results


| Feature | Test Case | Method | Expected Status | Result |
|---------|-----------|--------|-----------------|--------|
| Users | Create User | POST | 201 Created | PASSED |
| Users | Duplicate Email | POST | 400 Bad Request | PASSED |
| Amenities | List Amenities | GET | 200 OK | PASSED |
| Places | Create Place | POST | 201 Created | PASSED |
| Reviews | Invalid Rating (6) | POST | 400 Bad Request | PASSED |

## 4. Execution
Automated tests were executed using the `unittest` framework:
- `test_api.py`: Validates API response codes and JSON structure.
- `tests_hbnb.py`: Validates core business logic and relationships.

## 5. Conclusion
All endpoints are functional, and data validation is strictly enforced as per the requirements.
