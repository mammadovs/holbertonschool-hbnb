# HBnB Evolution: Complete Technical Blueprint

## Introduction
Welcome to the technical design documentation for the **HBnB Evolution** project. This document serves as a comprehensive guide for the development team, outlining the system's architecture, core business logic, and interaction patterns. 

Our goal is to build a scalable, Airbnb-like platform where users can manage properties, post reviews, and discover amenities. To ensure long-term maintainability, this blueprint follows a strict layered architecture, keeping the "how" (technical details) separate from the "what" (business value).

---

## 1. High-Level System Architecture

To handle the complexity of the HBnB ecosystem, I have adopted a **Three-Layer Architecture**. This design ensures that each part of the system has a single responsibility.

### Architectural Diagram
The following package diagram shows the three main layers and how they interact through a central gateway.

```mermaid
classDiagram
    direction TB

    class PresentationLayer {
        <<Layer>>
        +REST_API
        +Controllers
    }

    class HBnBFacade {
        <<Interface>>
        +Unified_Entry_Point
    }

    class BusinessLogicLayer {
        <<Layer>>
        +Domain_Models
        +Business_Rules
    }

    class PersistenceLayer {
        <<Layer>>
        +Database_Access
        +File_Storage
    }

    PresentationLayer --> HBnBFacade : API Calls
    HBnBFacade --> BusinessLogicLayer : Validation & Logic
    HBnBFacade --> PersistenceLayer : Data Storage
```

```mermaid
classDiagram
    class BaseModel {
        <<Abstract>>
        +UUID4 id
        +DateTime created_at
        +DateTime updated_at
        +save()
        +update()
    }

    class User {
        +String email
        +String password
        +Boolean is_admin
        +register()
    }

    class Place {
        +String title
        +Float price
        +Float latitude
        +Float longitude
    }

    class Review {
        +Integer rating
        +String comment
    }

    class Amenity {
        +String name
    }

    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity

    User "1" --> "0..*" Place : hosts
    User "1" --> "0..*" Review : writes
    Place "1" --> "0..*" Review : receives
    Place "*" --> "*" Amenity : features
```

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant F as Facade
    participant D as DB
    C->>A: POST /users
    A->>F: register_user(data)
    F->>F: Validate Unique Email
    F->>D: save(User)
    D-->>F: Success
    F-->>A: User Object
    A-->>C: 201 Created
```

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant F as Facade
    participant D as DB
    C->>A: POST /places
    A->>F: create_place(data)
    F->>D: save(Place)
    D-->>F: Success
    F-->>A: Place Object
    A-->>C: 201 Created
```

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant F as Facade
    participant D as DB
    C->>A: POST /reviews
    A->>F: submit_review(data)
    F->>D: Check User & Place
    D-->>F: Verified
    F->>D: save(Review)
    D-->>F: Success
    F-->>A: Review Object
    A-->>C: 201 Created
```

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant F as Facade
    participant D as DB
    C->>A: GET /places
    A->>F: get_places(criteria)
    F->>D: find_all(criteria)
    D-->>F: Data List
    F-->>A: JSON Result
    A-->>C: 200 OK
```
