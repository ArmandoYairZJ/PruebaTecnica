from modules.domains.Productos.models import product
from sqlalchemy.ext.asyncio import AsyncSession
from modules.domains.Productos.schema import ProductCreate

async def create_product(db: AsyncSession, data: ProductCreate):
    productInstance = product(**data.model_dump())
    db.add(productInstance)
    await db.commit()
    await db.refresh(productInstance)
    return productInstance

async def get_all_products(db: AsyncSession):
    return db.query(product).all()

async def get_product_by_id(db: AsyncSession, product_id: int):
    return db.query(product).filter(product.id == product_id).first()

async def update_product(db: AsyncSession, product_id: int, data: ProductCreate):
    productInstance = db.query(product).filter(product.id == product_id).first()
    if productInstance:
        for key, value in data.model_dump().items():
            setattr(productInstance, key, value)
        await db.commit()
        await db.refresh(productInstance)
    return productInstance

async def delete_product(db: AsyncSession, product_id: int):
    productInstance = db.query(product).filter(product.id == product_id).first()
    if productInstance:
        await db.delete(productInstance)
        await db.commit()
    return productInstance