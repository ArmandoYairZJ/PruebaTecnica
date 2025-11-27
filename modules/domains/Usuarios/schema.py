from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class rolEnum(Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class UserBase(BaseModel):
    username:str
    email:str
    rol:rolEnum

class UserInDB(UserBase):
    password:str

class UserCreate(UserBase):
    username:str
    email:str
    password:str

class User(UserBase):
    id:int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
