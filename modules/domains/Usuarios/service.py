from modules.domains.Usuarios.models import user
from modules.domains.Usuarios.schema import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def create_user(db: AsyncSession, data: UserCreate):
    userInstance = user(**data.model_dump())
    db.add(userInstance)
    await db.commit()
    await db.refresh(userInstance)
    return userInstance

async def get_user(db:AsyncSession):
    result = await db.execute(select(user))
    return result.scalars().all()

async def get_user_id(db:AsyncSession, userId: int):
    result = await db.execute(
        select(user).where(user.id == userId)
    )
    return result.scalar_one_or_none()

async def update_user(db:AsyncSession, userId:int, data:UserCreate):
    result = await db.execute(
        select(user).where(user.id == userId)
    )
    userInstance = result.scalar_one_or_none()
    if not userInstance:
        return None
    for key, value in data.model_dump().items():
        setattr(userInstance, key, value)
    await db.commit()
    await db.refresh(userInstance)
    return userInstance

async def delete_user(db:AsyncSession, userId:int):
    result = await db.execute(
        select(user).where(user.id == userId)
    )
    userInstance = result.scalar_one_or_none()
    if not userInstance:
        return None
    await db.delete(userInstance)
    await db.commit()
    return userInstance