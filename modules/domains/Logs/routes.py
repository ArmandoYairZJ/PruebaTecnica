from fastapi import APIRouter, Depends, HTTPException
from modules.domains.Logs.schema import Log, LogCreate
from modules.domains.Logs.service import (
    get_log_by_id,
    get_logs,

)
from modules.core.config.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/logs", response_model=list[Log])
async def get_all_logs(db: AsyncSession = Depends(get_db)):
    return await get_logs(db)


@router.get("/logs/{log_id}", response_model=Log)
async def read_log(log_id: int, db: AsyncSession = Depends(get_db)):
    log_obj = await get_log_by_id(db, log_id)
    if log_obj is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return log_obj
