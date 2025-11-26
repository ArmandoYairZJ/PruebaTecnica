from fastapi import APIRouter, Depends, HTTPException
from modules.domains.Productos.schema import ProductCreate, Product
from modules.domains.Productos.service import create_product, get_product_by_id, get_all_products, delete_product, update_product
from modules.core.config.db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/products", response_model=list[Product])
def get_products(db: Session = Depends(get_db)):
    return get_all_products(db)

@router.get("/products/{product_id}", response_model=Product)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    productQuerySet = get_product_by_id(db, id)
    if  productQuerySet:
        return productQuerySet
    raise HTTPException(status_code=404, detail="Product not found")

@router.post("/products", response_model=Product)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)

@router.put("/products/{product_id}", response_model=Product)
def update_product_by_id(id: int, product: ProductCreate, db: Session = Depends(get_db)):
    productUpdate = get_product_by_id(db, id)
    if not productUpdate:
        raise HTTPException(status_code=404, detail="Product not found")
    return update_product(db, id, product)

@router.delete("/products/{product_id}", response_model=Product)
def delete_product_by_id(id: int, db: Session = Depends(get_db)):
    productDelete = delete_product(db, id)
    if delete_product:
        return productDelete
    raise HTTPException(status_code=404, detail="Product not found")
