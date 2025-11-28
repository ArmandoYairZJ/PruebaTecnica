from modules.domains.Usuarios.models import user
from modules.domains.Usuarios.schema import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from sqlalchemy import select

async def get_user(db:AsyncSession):
    result = await db.execute(select(user))
    return result.scalars().all()

async def get_user_id(db:AsyncSession, userId: int):
    result = await db.execute(
        select(user).where(user.id == userId)
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