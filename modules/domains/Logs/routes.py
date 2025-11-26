from fastapi import APIRouter, Depends, HTTPException
from modules.domains.Logs.schema import Log, LogCreate
from modules.domains.Logs.service import (
    create_log,
    get_log_by_id,
    get_logs,
    delete_log,
    update_log
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


@router.post("/logs", response_model=Log)
async def create_new_log(data: LogCreate, db: AsyncSession = Depends(get_db)):
    return await create_log(db, data)


@router.put("/logs/{log_id}", response_model=Log)
async def update_existing_log(log_id: int, data: LogCreate, db: AsyncSession = Depends(get_db)):
    updated = await update_log(db, log_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Log not found")
    return updated


@router.delete("/logs/{log_id}", response_model=Log)
async def delete_log_by_id(log_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_log(db, log_id)
    if deleted:
        return deleted
    raise HTTPException(status_code=404, detail="Log not found")
