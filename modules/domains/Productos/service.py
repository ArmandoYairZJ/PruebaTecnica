from modules.domains.Productos.models import product
from sqlalchemy.ext.asyncio import AsyncSession
from modules.domains.Productos.schema import ProductCreate
from sqlalchemy import select


async def create_product(db: AsyncSession, data: ProductCreate):
    productInstance = product(**data.model_dump())
    db.add(productInstance)
    await db.commit()
    await db.refresh(productInstance)
    return productInstance

async def get_all_products(db: AsyncSession):
    result = await db.execute(select(product))
    return result.scalars().all()

async def get_product_by_id(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(product).where(product.id == product_id)
    )
    return result.scalar_one_or_none()

async def update_product(db: AsyncSession, product_id: int, data: ProductCreate):
    result = await db.execute(
        select(product).where(product.id == product_id)
    )
    productInstance = result.scalar_one_or_none()

    if not productInstance:
        return None

    for key, value in data.model_dump().items():
        setattr(productInstance, key, value)

    await db.commit()
    await db.refresh(productInstance)
    return productInstance

async def delete_product(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(product).where(product.id == product_id)
    )
    productInstance = result.scalar_one_or_none()

    if not productInstance:
        return None

    await db.delete(productInstance)
    await db.commit()
    return productInstance