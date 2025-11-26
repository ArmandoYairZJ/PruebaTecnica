from fastapi import APIRouter, Depends, HTTPException
from modules.domains.Usuarios.schema import UserCreate, User
from modules.domains.Usuarios.service import (
    create_user,
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
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user_obj = await get_user_id(db, user_id)
    if user_obj:
        return user_obj
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/users", response_model=User)
async def create_new_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, data)


@router.put("/users/{user_id}", response_model=User)
async def update_user_by_id(user_id: int, data: UserCreate, db: AsyncSession = Depends(get_db)):
    user_obj = await update_user(db, user_id, data)
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    return user_obj


@router.delete("/users/{user_id}", response_model=User)
async def delete_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user_obj = await delete_user(db, user_id)
    if user_obj:
        return user_obj
    raise HTTPException(status_code=404, detail="User not found")
