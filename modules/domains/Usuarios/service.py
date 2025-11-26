from modules.domains.Usuarios.models import user
from  sqlalchemy.orm import Session
from modules.domains.Usuarios.schema import userCreate

def create_user(db: Session, data: userCreate):
    userInstance = user(**data.model_dump())
    db.add(userInstance)
    db.commit()
    db.refresh(userInstance)
    return userInstance

def get_user(db:Session):
    return db.query(user).all()

def get_user_id(db:Session, userId: int):
    return db.query(user).filter(user.id == userId).first()

def update_user(db:Session, userId:int, data:userCreate):
    userQuerySet = db.query(user).filter(user.id == userId).first()
    if userQuerySet:
        for key, vallue in user.model_dump().items():
            setattr(userQuerySet, key, vallue)
        db.commit()
        db.refresh(userQuerySet)
    return userQuerySet

def delete_user(db:Session, userId:int):
    userQuerySet = db.query(user).filter(user.id == userId).first()
    if userQuerySet:
        db.delete(userQuerySet)
        db.commit()
    return userQuerySet