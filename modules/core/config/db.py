from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from pydantic_settings import BaseSettings
import os
from sqlalchemy import create_engine

class Settings(BaseSettings):
    #Base de datos
    DATABASE_URL: str
    class Config:
        env_file = ".env"
   
    # JWT
    secret_key: str = "secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

settings = Settings()

Base = declarative_base()

# Detecta si estamos corriendo migraciones
if os.environ.get("RUNNING_MIGRATIONS", "0") == "1":
    engine = create_engine(settings.DATABASE_URL.replace("asyncpg+", ""))
else:
    engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine if "async" in str(type(engine)) else None,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)