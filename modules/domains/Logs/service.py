from modules.domains.Logs.models import log
from sqlalchemy.ext.asyncio import AsyncSession
from modules.domains.Logs.schema import LogCreate

async def create_log(db: AsyncSession, data: LogCreate):
    logInstance = log(**data.model_dump())
    db.add(logInstance)
    await db.commit()
    await db.refresh(logInstance)
    return logInstance

async def get_logs(db:AsyncSession):
    return db.query(log).all()

async def get_log_by_id(db:AsyncSession, logId: int):
    return db.query(log).filter(log.id == logId).first()

async def update_log(db:AsyncSession, logId:int, data: LogCreate):
    logInstance = db.query(log).filter(log.id == logId).first()
    for key, value in data.model_dump().items():
        setattr(logInstance, key, value)
    await db.commit()
    await db.refresh(logInstance)
    return logInstance

async def delete_log(db:AsyncSession, logId:int):
    logInstance = db.query(log).filter(log.id == logId).first()
    if logInstance:
        await db.delete(logInstance)
        await db.commit()
    return logInstance