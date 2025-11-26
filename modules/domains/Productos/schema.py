from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    nombre: str
    precio: float
    marca: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    delete_at: Optional[datetime] = None

    class Config:
        from_attributes = True