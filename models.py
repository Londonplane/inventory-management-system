from pydantic import BaseModel, Field

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
        from_attributes = True