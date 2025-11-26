from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.core.routes import router as MainRouter
from scalar_fastapi import get_scalar_api_reference, Layout

app = FastAPI(
    docs_url=None,
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
