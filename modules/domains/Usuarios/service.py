from modules.domains.Usuarios.models import user
from modules.domains.Usuarios.schema import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from modules.domains.Logs.models import log
from fastapi import HTTPException
from datetime import datetime, timezone
from sqlalchemy import select

async def get_user(db:AsyncSession):
    result = await db.execute(select(user).where(user.is_deleted == False))
    return result.scalars().all()

async def get_user_id(db:AsyncSession, userId: int):
    result = await db.execute(
        select(user).where(user.id == userId, user.is_deleted == False)
    )
    return result.scalar_one_or_none()

async def update_user(db: AsyncSession, userId: str, data: UserCreate):
    result = await db.execute(
        select(user).where(user.id == userId)
    )
    userInstance = result.scalar_one_or_none()
    if not userInstance:
        return None
    bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    fields = data.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in fields.items():
        if key == "created_at":
            continue
        if key == "rol" and hasattr(value, "value"):
            value = value.value
        if key == "password":
            if not value:
                continue
            value = bcrypt_context.hash(value[:72])
            key = "hashed_password"
        if isinstance(value, str) and value == "":
            continue
        setattr(userInstance, key, value)
    await db.commit()
    await db.refresh(userInstance)
    return userInstance

async def delete_user(db: AsyncSession, userId: str):
    result = await db.execute(select(user).where(user.id == userId))
    userInstance = result.scalar_one_or_none()
    if not userInstance:
        return None
    
    if getattr(userInstance, "is_deleted", False):
        raise HTTPException(status_code=400, detail="Es usuario ya esta eliminado.")

    has_logs = await db.execute(select(log).where(log.user_id == userId).limit(1))
    if has_logs.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="No se puede eliminar: existen logs asociados")

    userInstance.is_deleted = True
    userInstance.deleted_at = datetime.now(timezone.utc) 
    await db.commit()
    await db.refresh(userInstance)
    return userInstance