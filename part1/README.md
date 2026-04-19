# HBnB Evolution: Technical Design Document

## Introduction
This document serves as the architectural foundation for the HBnB project. My goal here is to map out how the system components interact and how the data is structured within the core business logic. I've adopted a layered approach to ensure the code stays clean, maintainable, and easy to scale as we add more features.

---

## 1. High-Level Architecture (Package Diagram)

For the overall structure, I decided to use a **three-layer architecture**. This helps in keeping the user interface (API) separate from the actual "brain" of the app and the database storage logic.

To keep these layers from becoming a tangled mess, I implemented the **Facade Pattern**. Instead of the API talking to every single model or repository, it goes through a single entry point—the Facade. This simplifies the workflow and keeps the layers decoupled.

```mermaid
classDiagram
    direction TB

    class PresentationLayer {
        <<Layer>>
        +API_Endpoints
        +Service_Controllers
    }

    class HBnBFacade {
        <<Interface>>
        +create_user()
        +register_place()
        +post_review()
        +add_amenity()
    }

    class BusinessLogicLayer {
        <<Layer>>
        +Domain_Models
        +Internal_Validation
    }

    class PersistenceLayer {
        <<Layer>>
        +Database_Operations
        +Data_Repositories
    }

    PresentationLayer --> HBnBFacade : API Requests
    HBnBFacade --> BusinessLogicLayer : Orchestrates Logic
    HBnBFacade --> PersistenceLayer : Data Persistence


classDiagram
    class BaseModel {
        <<Abstract>>
        +UUID4 id
        +DateTime created_at
        +DateTime updated_at
        +save()
        +update(data)
    }

    class User {
        +String first_name
        +String last_name
        +String email
        +String password
        +Boolean is_admin
        +register()
        +update_profile()
    }

    class Place {
        +String title
        +String description
        +Float price
        +Float latitude
        +Float longitude
        +create_place()
        +list_all()
    }

    class Review {
        +Integer rating
        +String comment
        +post_review()
    }

    class Amenity {
        +String name
        +String description
        +list_amenities()
    }

    BaseModel <|-- User : Generalization
    BaseModel <|-- Place : Generalization
    BaseModel <|-- Review : Generalization
    BaseModel <|-- Amenity : Generalization

    User "1" --> "0..*" Place : hosts
    User "1" --> "0..*" Review : writes
    Place "1" --> "0..*" Review : receives
    Place "*" --> "*" Amenity : includes

