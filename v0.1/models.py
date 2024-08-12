from pydantic import BaseModel, Field
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: str = None
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

class SaleBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    sale_date: datetime

    class Config:
        orm_mode = True

class InventoryReport(BaseModel):
    product_id: int
    product_name: str
    current_quantity: int
    total_sales: int