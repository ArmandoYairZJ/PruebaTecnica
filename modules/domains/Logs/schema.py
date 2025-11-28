from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class LogBase(BaseModel):
    descripcion: str
    user_id: str
    product_id: int
    old_data: Optional[Any] = None
    new_data: Optional[Any] = None

class LogCreate(LogBase):
    pass

class Log(LogBase):
    folio:int
    created_at: datetime

    class Config:
        from_attributes = True