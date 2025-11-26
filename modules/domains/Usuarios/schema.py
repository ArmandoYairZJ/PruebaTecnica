from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class rolEnum(Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class UserBase(BaseModel):
    nombre:str
    email:str
    rol:rolEnum

class UserCreate(UserBase):
    password:str

class User(UserBase):
    id:int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    