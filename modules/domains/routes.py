from fastapi import APIRouter
from modules.domains.Usuarios.routes import router as UsuariosRouter

router = APIRouter()  
router.include_router(UsuariosRouter, prefix="/usuarios", tags=["Usuarios"])
