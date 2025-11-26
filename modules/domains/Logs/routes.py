from fastapi import APIRouter, Depends, HTTPException
from modules.domains.Logs.schema import Log, LogCreate
from modules.domains.Logs.service import create_log, get_log_by_id, get_logs, delete_log, update_log
from modules.core.config.db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/logs", response_model=list[Log])
def get_all_logs(db: Session = Depends(get_db)):
    return get_logs(db)

@router.get("/logs/{log_id}", response_model=Log)
def read_log(id: int, db: Session = Depends(get_db)):
    logQuerySet = get_log_by_id(db, id)
    if logQuerySet is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return logQuerySet

@router.post("/logs", response_model=Log)
def create_new_log(log: LogCreate, db: Session = Depends(get_db)):
    return create_log(db, log)

@router.put("/logs/{log_id}", response_model=Log)
def update_existing_log(id: int, data: LogCreate, db: Session = Depends(get_db)):
    logUpdate = get_log_by_id(db, id, data)
    if not logUpdate:
        raise HTTPException(status_code=404, detail="Log not found")
    return logUpdate

@router.delete("/logs/{log_id}", response_model=Log)
def delete_user_by_id(id: int, db: Session = Depends(get_db)):
    deleteLog = get_log_by_id(db, id)
    if  deleteLog:
        return deleteLog
    raise HTTPException(status_code=404, detail="Log not found")    
        