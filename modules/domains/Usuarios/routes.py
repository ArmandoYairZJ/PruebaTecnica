from fastapi import APIRouter, Depends, HTTPException, Response
from modules.domains.Usuarios.schema import UserCreate, User
from modules.domains.Usuarios.service import (
    get_user,
    get_user_id,
    update_user,
    delete_user
)
from modules.core.config.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get("/users", response_model=list[User])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await get_user(db)

@router.get("/users/{user_id}", response_model=User)
async def get_user_by_id(user_id: str, db: AsyncSession = Depends(get_db)):
    userObject = await get_user_id(db, user_id)
    if userObject:
        return userObject
    raise HTTPException(status_code=404, detail="Usuario No Encontrado")

@router.put("/users/{user_id}", response_model=dict)
async def update_user_by_id(user_id: str, data: UserCreate, db: AsyncSession = Depends(get_db)):
    update = await update_user(db, user_id, data)
    if not update:
        raise HTTPException(status_code=404, detail="Usuario No Encontrado")
    return {"message": f"Usuario {update.id} actualizado exitosamente"}

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user_by_id(user_id: str, db: AsyncSession = Depends(get_db)):
    delete = await delete_user(db, user_id)
    if delete:
        return {"message": f"Usuario {delete.id} eliminado exitosamente"}
    raise HTTPException(status_code=404, detail="Usuario No Encontrado")
