from fastapi import FastAPI, HTTPException, Depends
from typing import List
import sqlite3
from models import Product, ProductCreate
from database import create_connection, init_db

app = FastAPI()

# Database connection
def get_db():
    conn = create_connection()
    try:
        yield conn
    finally:
        conn.close()

# 确保了在 FastAPI 应用开始接收请求之前，数据库已经被正确初始化
@app.on_event("startup")
async def startup_event():
    init_db()

## API routes

@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Management System"}

# Product Management

# insert into new product
@app.post("/products/", response_model=Product)
def create_product(product: ProductCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO products (name, description, price, quantity)
        VALUES (?, ?, ?, ?)
    """, (product.name, product.description, product.price, product.quantity))
    db.commit()
    product_id = cursor.lastrowid
    return {**product.dict(), "id": product_id}

# get all products
@app.get("/products/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products LIMIT ? OFFSET ?", (limit, skip))
    products = cursor.fetchall()
    return [Product(id=row[0], name=row[1], description=row[2], price=row[3], quantity=row[4]) for row in products]

# get specific product
@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(id=product[0], name=product[1], description=product[2], price=product[3], quantity=product[4])

# update product
@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        UPDATE products
        SET name = ?, description = ?, price = ?, quantity = ?
        WHERE id = ?
    """, (product.name, product.description, product.price, product.quantity, product_id))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {**product.dict(), "id": product_id}

# delete product
@app.delete("/products/{product_id}", response_model=dict)
def delete_product(product_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}