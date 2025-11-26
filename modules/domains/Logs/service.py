from modules.domains.Logs.models import log
from sqlalchemy.orm import Session
from modules.domains.Logs.schema import LogCreate

def create_log(db: Session, data: LogCreate):
    logInstance = log(**data.model_dump())
    db.add(logInstance)
    db.commit()
    db.refresh(logInstance)
    return logInstance

def get_logs(db:Session):
    return db.query(log).all()

def get_log_by_id(db:Session, logId: int):
    return db.query(log).filter(log.id == logId).first()

def update_log(db:Session, logId:int, data: LogCreate):
    logInstance = db.query(log).filter(log.id == logId).first()
    for key, value in data.model_dump().items():
        setattr(logInstance, key, value)
    db.commit()
    db.refresh(logInstance)
    return logInstance

def delete_log(db:Session, logId:int):
    logInstance = db.query(log).filter(log.id == logId).first()
    if logInstance:
        db.delete(logInstance)
        db.commit()
    return logInstance