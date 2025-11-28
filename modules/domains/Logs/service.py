from modules.domains.Logs.models import log
from sqlalchemy.ext.asyncio import AsyncSession
from modules.domains.Logs.schema import LogCreate
from sqlalchemy import select

async def create_log(db: AsyncSession, data: LogCreate):
    payload = data.model_dump(exclude_none=True)
    model_cols = {c.name for c in log.__table__.columns}
    kwargs = {k: v for k, v in payload.items() if k in model_cols}
    logInstance = log(**kwargs)
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
