# HBnB Application - High-Level Package Diagram

## 1. Package Diagram

The following diagram illustrates the three-layer architecture of the HBnB application. It highlights the separation of concerns and the use of the Facade pattern to streamline communication between the layers.

```mermaid
classDiagram
    class Presentation_Layer {
        <<Interface>>
        +API_Endpoints
        +Service_Controllers
        note: Handles HTTP requests/responses
    }
    class Business_Logic_Layer {
        +HBnB_Facade
        +User_Model
        +Place_Model
        +Review_Model
        +Amenity_Model
        note: Contains core business logic
    }
    class Persistence_Layer {
        +Data_Repository
        +Storage_Engine
        note: Handles DB operations
    }

    Presentation_Layer --> Business_Logic_Layer : "Calls via Facade"
    Business_Logic_Layer --> Persistence_Layer : "Database CRUD operations"

