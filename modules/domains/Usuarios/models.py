from modules.core.config.db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship
from uuid import uuid4

class user(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    rol = Column(String, index=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)                    
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    logs = relationship("log", back_populates="user")