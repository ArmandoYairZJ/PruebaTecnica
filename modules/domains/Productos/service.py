from fastapi import HTTPException
from modules.domains.Productos.models import product
from sqlalchemy.ext.asyncio import AsyncSession
from modules.domains.Productos.schema import ProductCreate
from modules.domains.Logs.service import create_log
from modules.domains.Logs.schema import LogCreate
from datetime import datetime
from sqlalchemy import select


async def create_product(db: AsyncSession, data: ProductCreate):
    fields = data.model_dump(exclude_unset=True, exclude_none=True)
    if "stock" in fields:
        try:
            fields["stock"] = int(fields["stock"])
        except (TypeError, ValueError):
            raise HTTPException(status_code=400, detail="El campo 'stock' debe ser un entero")
        if fields["stock"] < 0:
            raise HTTPException(status_code=400, detail="El stock no puede ser negativo")
    productInstance = product(**data.model_dump())
    db.add(productInstance)
    await db.commit()
    await db.refresh(productInstance)
    return productInstance

async def get_all_products(db: AsyncSession):
    result = await db.execute(select(product).where(product.is_deleted == False))
    return result.scalars().all()

async def get_product_by_id(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(product).where(product.id == product_id)
    )
    return result.scalar_one_or_none()

async def update_product(db: AsyncSession, product_id: int, data: ProductCreate, userId: str, descripcion: str):
    result = await db.execute(
        select(product).where(product.id == product_id)
    )
    productInstance = result.scalar_one_or_none()
    if not productInstance:
        return None
    
    def _serialize(v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v

    old_data = {c.name: _serialize(getattr(productInstance, c.name)) for c in product.__table__.columns}

    fields = data.model_dump(exclude_unset=True, exclude_none=True)

    changed = False
    for key, value in fields.items():
        if key == "created_at":  
            continue

        if key == "stock":
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise HTTPException(status_code=400, detail="El campo 'stock' debe ser un entero")
            if value < 0:
                raise HTTPException(status_code=400, detail="El stock no puede ser negativo")
        
        if isinstance(value, str) and value == "":
            continue
        setattr(productInstance, key, value)
        changed = True

    if not changed:
        return productInstance
    
    productInstance.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(productInstance)

    new_data = {c.name: _serialize(getattr(productInstance, c.name)) for c in product.__table__.columns}

    log_payload = LogCreate(
        descripcion=descripcion,
        user_id=userId or "system",
        product_id=productInstance.id,
        old_data=old_data,
        new_data=new_data
    )
    await create_log(db, log_payload)

    return productInstance

async def delete_product(db: AsyncSession, product_id: int, userId: str, descripcion: str):
    result = await db.execute(
        select(product).where(product.id == product_id)
    )
    productInstance = result.scalar_one_or_none()

    if not productInstance:
        return None

    if getattr(productInstance, "is_deleted", False):
        raise HTTPException(status_code=400, detail="Es producto ya se encuentra eliminado.")

    def _serialize(v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v

    old_data = {c.name: _serialize(getattr(productInstance, c.name)) for c in product.__table__.columns}

    if not getattr(productInstance, "is_deleted", False):
        productInstance.is_deleted = True
    productInstance.delete_at = datetime.utcnow()

    await db.commit()
    await db.refresh(productInstance)

    new_data = {c.name: _serialize(getattr(productInstance, c.name)) for c in product.__table__.columns}

    log_payload = LogCreate(
        descripcion=descripcion,
        user_id=userId or "system",
        product_id=productInstance.id,
        old_data=old_data,
        new_data=new_data
    )
    await create_log(db, log_payload)

    return productInstance