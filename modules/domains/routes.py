from fastapi import APIRouter
from modules.domains.Usuarios.routes import router as UsuariosRouter
from modules.domains.Productos.routes import router as ProductosRouter
from modules.domains.Logs.routes import router as LogsRouter

router = APIRouter()  

router.include_router(UsuariosRouter, prefix="/usuarios", tags=["Usuarios"])
router.include_router(ProductosRouter, prefix="/productos", tags=["Productos"])
router.include_router(LogsRouter, prefix="/logs", tags=["Logs"])