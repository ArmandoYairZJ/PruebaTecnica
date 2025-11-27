from fastapi import FastAPI, Depends, HTTPException,  status
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from modules.core.routes import router as MainRouter
from scalar_fastapi import get_scalar_api_reference, Layout
from modules.auth.auth import router as AuthRouter
from sqlalchemy.orm import Session as Ses
from modules.auth.auth import get_current_user
from modules.core.config.db import get_db

db_dependency = Annotated [Ses, Depends(get_db)]
user_dependency = Annotated [dict, Depends(get_current_user)]

app = FastAPI(
    docs_url=None,
    redoc_url=None
)
app.include_router(AuthRouter)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hola")
async def hola(user: Annotated[dict, Depends(get_current_user)]):
    return {"mensaje": "Hello World"}

@app.get("/docs", include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(
        title="API Prueba Tecnica Coppel",
        layout=Layout.MODERN,
        dark_mode=True,
        show_sidebar=True,
        default_open_all_tags=True,
        hide_models=True
    )

@app.get("/", tags=["Root"])
async def read_root():
    return {"Prueba Tecnica Coppel": "API de usuarios y productos"}

app.include_router(MainRouter)
