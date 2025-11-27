from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from modules.core.config.db import get_db, settings
from modules.domains.Usuarios.models import user
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.future import select

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateUserRequest(BaseModel):
    email: str
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

db_dependency = Annotated[AsyncSession, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = user(
        username=create_user_request.username,
        email=create_user_request.email,
        hashed_password=bcrypt_context.hash(create_user_request.password[:72]),
        rol="USER"
    )
    db.add(create_user_model)
    await db.commit()
    await db.refresh(create_user_model)
    return {
        "id": create_user_model.id,
        "email": create_user_model.email,
        "username": create_user_model.username}

@router.post("/token", response_model=Token)
async def login_for_access_token(data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user_obj = await authenticate_user(db, data.username, data.password)
    if not user_obj: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        )
    token = create_access_token(user_obj.email, user_obj.id, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"} 

async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(
        select(user).where(user.email == email)
    )
    user_obj = result.scalars().first()
    if not user_obj:
        return False
    if not bcrypt_context.verify(password, user_obj.hashed_password):
        return False
    return user_obj

async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(
        select(user).where(user.email == email)
    )
    user_obj = result.scalars().first()
    if not user_obj:
        return False
    if not bcrypt_context.verify(password, user_obj.hashed_password):
        return False
    return user_obj


def create_access_token(email: str, user_id: str, expire_delta: timedelta):
    encode = { 'sub': email, 'user_id': user_id }
    expire = datetime.utcnow() + expire_delta
    encode.update({"exp": expire})
    return jwt.encode(encode, settings.secret_key, algorithm=settings.algorithm)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        if email is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        return {'email': email, 'id': user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        )