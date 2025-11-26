from modules.domains.Usuarios.models import user
from  sqlalchemy.orm import Session
from modules.domains.Usuarios.schema import UserCreate

def create_user(db: Session, data: UserCreate):
    userInstance = user(**data.model_dump())
    db.add(userInstance)
    db.commit()
    db.refresh(userInstance)
    return userInstance

def get_user(db:Session):
    return db.query(user).all()

def get_user_id(db:Session, userId: int):
    return db.query(user).filter(user.id == userId).first()

def update_user(db:Session, userId:int, data:UserCreate):
    userInstance = db.query(user).filter(user.id == userId).first()
    if userInstance:
        for key, value in user.model_dump().items():
            setattr(userInstance, key, value)
        db.commit()
        db.refresh(userInstance)
    return userInstance

def delete_user(db:Session, userId:int):
    userInstance = db.query(user).filter(user.id == userId).first()
    if userInstance:
        db.delete(userInstance)
        db.commit()
    return userInstance