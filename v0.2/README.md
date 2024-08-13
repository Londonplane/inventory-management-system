# Inventory Management System - v0.1

This is the initial version of the Inventory Management System, implementing basic CRUD operations for product management.

## Features

- Product Management (CRUD operations)
  - Create new products
  - Retrieve product information
  - Update product details
  - Delete products

## Project Structure

```
v0.1/
├── main.py         # FastAPI application and route definitions
├── models.py       # Pydantic models for data validation
├── database.py     # Database connection and initialization
├── inventory.db    # SQLite database file
├── note.txt        # Development notes for v0.1
└── README.md       # Version-specific documentation
```

## Running the Application

From this directory, run:

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

For more detailed information about the project, please refer to the main README in the root directory.