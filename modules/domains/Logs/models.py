from modules.core.config.db import Base
from sqlalchemy import  Column, Integer, String, ForeignKey, JSON, TIMESTAMP, func
from sqlalchemy.orm import relationship

class log(Base):
    __tablename__ = "logs"

    folio = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    old_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    user = relationship("user", back_populates="logs")
    product = relationship("product", back_populates="logs")