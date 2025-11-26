from fastapi import APIRouter
from modules.domains.Productos.routes import router as ProductosRouter
from modules.domains.Usuarios.routes import router as UsuariosRouter

router = APIRouter()

router.include_router(ProductosRouter, prefix="/productos", tags=["Productos"])
router.include_router(UsuariosRouter, prefix="/usuarios", tags=["Usuarios"])