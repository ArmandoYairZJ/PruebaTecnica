from pydantic import BaseModel
from enum import Enum

class rolEnum(Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class userBase(BaseModel):
    username:str
    email:str
    password:str
    rol:rolEnum

class userCreate(userBase):
    pass

class user(userBase):
    id:int

    class Config:
        from_attributes = True

    