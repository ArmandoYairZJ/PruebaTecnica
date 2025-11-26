from fastapi import APIRouter
from modules.domains.routes import router as DomainsRouter

router = APIRouter()

router.include_router(DomainsRouter, prefix="/domains",)