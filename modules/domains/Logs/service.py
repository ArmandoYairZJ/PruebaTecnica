from modules.domains.Logs.models import log
from sqlalchemy.ext.asyncio import AsyncSession
from modules.domains.Logs.schema import LogCreate
from sqlalchemy import select

async def create_log(db: AsyncSession, data: LogCreate):
    logInstance = log(**data.model_dump())
    db.add(logInstance)
    await db.commit()
    await db.refresh(logInstance)
    return logInstance

async def get_logs(db:AsyncSession):
    result = await db.execute(select(log))
    return result.scalars().all()

async def get_log_by_id(db:AsyncSession, logId: int):
    result = await db.execute(
        select(log).where(log.id == logId)
    )
    return result.scalar_one_or_none()

async def update_log(db:AsyncSession, logId:int, data: LogCreate):
    result = await db.execute(
        select(log).where(log.id == logId)
    )
    logInstance = result.scalar_one_or_none()
    if not logInstance:
        return None
    for key, value in data.model_dump().items():
        setattr(logInstance, key, value)
    await db.commit()
    await db.refresh(logInstance)
    return logInstance

async def delete_log(db:AsyncSession, logId:int):
    result = await db.execute(
        select(log).where(log.id == logId)
    )
    logInstance = result.scalar_one_or_none()
    if not logInstance:
        return None
    await db.delete(logInstance)
    await db.commit()
    return logInstance