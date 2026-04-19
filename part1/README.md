# HBnB Evolution - Technical Documentation

## Introduction
This documentation provides a high-level architectural overview of the HBnB application. The project is designed using a layered architecture to ensure modularity, maintainability, and a clear separation of concerns between user interaction, business logic, and data storage.

## 1. High-Level Package Diagram

The diagram below illustrates the three-layer architecture of the HBnB application and the communication between these layers via the **Facade Pattern**.

```mermaid
classDiagram
    direction TB

    class PresentationLayer {
        <<Package>>
        +Services
        +API_Endpoints
    }

    class HBnBFacade {
        <<Facade Interface>>
        +create_user()
        +create_place()
        +submit_review()
        +manage_amenities()
    }

    class BusinessLogicLayer {
        <<Package>>
        +UserModel
        +PlaceModel
        +ReviewModel
        +AmenityModel
    }

    class PersistenceLayer {
        <<Package>>
        +DatabaseAccessObjects
        +DataStorage
    }

    PresentationLayer --> HBnBFacade : API Requests / Input
    HBnBFacade --> BusinessLogicLayer : Manages Business Rules
    HBnBFacade --> PersistenceLayer : Data Storage / Retrieval

