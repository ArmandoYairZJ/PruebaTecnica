from modules.core.config.db import Base
from sqlalchemy import  Column, Integer, String,Boolean, TIMESTAMP, func
from sqlalchemy.orm import relationship

class product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)

    precio = Column(Integer, index=True)
    marca = Column(String, index=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
    delete_at = Column(TIMESTAMP(timezone=True), nullable=True)
    logs = relationship("logs", back_populates="product")