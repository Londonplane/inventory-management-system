# Inventory Management System

## Project Overview

This is a simple Inventory Management System built with FastAPI and SQLite. It demonstrates basic CRUD operations for product management and lays the foundation for more advanced features.

## Version: v0.1

### Features

- Product Management (CRUD operations)
  - Create new products
  - Retrieve product information
  - Update product details
  - Delete products

### Tech Stack

- FastAPI: Web framework for building APIs
- SQLite: Lightweight database for data storage
- Pydantic: Data validation and settings management

## Project Structure

```
inventory_system/
│
├── main.py         # FastAPI application and route definitions
├── models.py       # Pydantic models for data validation
├── database.py     # Database connection and initialization
└── README.md       # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/inventory-management-system.git
   ```

2. Navigate to the project directory:
   ```
   cd inventory-management-system
   ```

3. Install the required dependencies:
   ```
   pip install fastapi uvicorn
   ```

## Running the Application

Run the following command in the project root directory:

```
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`. You can access the interactive API documentation at `http://localhost:8000/docs`.

## API Endpoints

- `GET /products/`: List all products
- `POST /products/`: Create a new product
- `GET /products/{product_id}`: Get details of a specific product
- `PUT /products/{product_id}`: Update a product
- `DELETE /products/{product_id}`: Delete a product

## Future Enhancements

- Inventory tracking
- Sales recording
- Reporting features
- User authentication and authorization

## Contributing

This project is primarily for educational purposes, demonstrating the evolution of a Python application. However, suggestions and discussions are welcome!

## License

This project is open source and available under the [MIT License](LICENSE).