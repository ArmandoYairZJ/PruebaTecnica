from fastapi import APIRouter, Depends, HTTPException
from modules.domains.Usuarios.schema import UserCreate, User
from modules.domains.Usuarios.service import create_user, get_user, get_user_id, update_user, delete_user
from modules.core.config.db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/users", response_model=list[User])
def get_all_users(db: Session = Depends(get_db)):
    return get_user(db)

@router.get("/users/{user_id}", response_model=User)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    userQuerySet = get_user_id(db, id)
    if userQuerySet:
        return userQuerySet
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/users", response_model=User)
def create_new_user(data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, data)

@router.put("/users/{user_id}", response_model=User)
def update_user_by_id(userId: int, data: UserCreate, db: Session = Depends(get_db)):
    userUpdate = update_user(db, userId, data)
    if not userUpdate:
        raise HTTPException(status_code=404, detail="User not found")
    return userUpdate

@router.delete("/users/{user_id}", response_model=User)
def delete_user_by_id(userId: int, db: Session = Depends(get_db)):
    userDelete = delete_user(db, userId)
    if userDelete:
        return userDelete
    raise HTTPException(status_code=404, detail="User not found")