from fastapi import FastAPI, HTTPException, Depends
from typing import List
import sqlite3
from datetime import datetime
from models import Product, ProductCreate, Sale, SaleCreate, InventoryReport
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

## API routes (add endpoints)

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


# Sales Management
@app.post("/sales/", response_model=Sale)
def create_sale(sale: SaleCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    
    # Check if product exists and has enough quantity
    cursor.execute("SELECT quantity FROM products WHERE id = ?", (sale.product_id,))
    product = cursor.fetchone()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if product[0] < sale.quantity:
        raise HTTPException(status_code=400, detail="Not enough inventory")
    
    # Create sale record
    cursor.execute("""
        INSERT INTO sales (product_id, quantity)
        VALUES (?, ?)
    """, (sale.product_id, sale.quantity))
    
    # Update product quantity
    cursor.execute("""
        UPDATE products
        SET quantity = quantity - ?
        WHERE id = ?
    """, (sale.quantity, sale.product_id))
    
    db.commit()
    sale_id = cursor.lastrowid
    return Sale(id=sale_id, product_id=sale.product_id, quantity=sale.quantity, sale_date=datetime.now())


# Inventory Management
@app.get("/inventory/", response_model=List[InventoryReport])
def get_inventory_report(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        SELECT p.id, p.name, p.quantity, COALESCE(SUM(s.quantity), 0) as total_sales
        FROM products p
        LEFT JOIN sales s ON p.id = s.product_id
        GROUP BY p.id
    """)
    inventory = cursor.fetchall()
    return [InventoryReport(product_id=row[0], product_name=row[1], current_quantity=row[2], total_sales=row[3]) 
            for row in inventory]
