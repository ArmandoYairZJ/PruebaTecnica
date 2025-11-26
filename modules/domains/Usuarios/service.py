from modules.domains.Usuarios.models import user
from modules.domains.Usuarios.schema import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession

async def create_user(db: AsyncSession, data: UserCreate):
    userInstance = user(**data.model_dump())
    db.add(userInstance)
    await db.commit()
    await db.refresh(userInstance)
    return userInstance

async def get_user(db:AsyncSession):
    return db.query(user).all()

async def get_user_id(db:AsyncSession, userId: int):
    return db.query(user).filter(user.id == userId).first()

async def update_user(db:AsyncSession, userId:int, data:UserCreate):
    userInstance = db.query(user).filter(user.id == userId).first()
    if userInstance:
        for key, value in user.model_dump().items():
            setattr(userInstance, key, value)
        await db.commit()
        await db.refresh(userInstance)
    return userInstance

async def delete_user(db:AsyncSession, userId:int):
    userInstance = db.query(user).filter(user.id == userId).first()
    if userInstance:
        await db.delete(userInstance)
        await db.commit()
    return userInstance