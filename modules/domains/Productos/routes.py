from fastapi import APIRouter, Depends, HTTPException
from modules.domains.Productos.schema import ProductCreate, Product
from modules.domains.Productos.service import (
    create_product,
    get_product_by_id,
    get_all_products,
    delete_product,
    update_product
)
from modules.core.config.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/products", response_model=list[Product])
async def get_products(db: AsyncSession = Depends(get_db)):
    return await get_all_products(db)


@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await get_product_by_id(db, product_id)
    if product:
        return product
    raise HTTPException(status_code=404, detail="Producto no encontrado")


@router.post("/products", response_model=Product)
async def create_new_product(data: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await create_product(db, data)


@router.put("/products/{product_id}", response_model=dict)
async def update_product_by_id(product_id: int, data: ProductCreate, description: str, user_id: str, db: AsyncSession = Depends(get_db)):
    update = await update_product(db, product_id, data, user_id, description)
    if not update:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": f"Producto {update.id} actualizado exitosamente"}

@router.delete("/products/{product_id}", response_model=dict)
async def delete_product_by_id(product_id: int, user_id: str, description: str, db: AsyncSession = Depends(get_db)):
    delete = await delete_product(db, product_id, user_id, description)
    if delete:
        return {"message": f"Producto {delete.id} eliminado exitosamente"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")