from modules.domains.Productos.models import product
from sqlalchemy.orm import Session
from modules.domains.Productos.schema import ProductCreate

def create_product(db: Session, data: ProductCreate):
    productInstance = product(**data.model_dump())
    db.add(productInstance)
    db.commit()
    db.refresh(productInstance)
    return productInstance

def get_all_products(db: Session):
    return db.query(product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(product).filter(product.id == product_id).first()

def update_product(db: Session, product_id: int, data: ProductCreate):
    productInstance = db.query(product).filter(product.id == product_id).first()
    if productInstance:
        for key, value in data.model_dump().items():
            setattr(productInstance, key, value)
        db.commit()
        db.refresh(productInstance)
    return productInstance

def delete_product(db: Session, product_id: int):
    productInstance = db.query(product).filter(product.id == product_id).first()
    if productInstance:
        db.delete(productInstance)
        db.commit()
    return productInstance