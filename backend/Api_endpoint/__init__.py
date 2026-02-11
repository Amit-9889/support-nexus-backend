from fastapi import APIRouter
from backend.Api_endpoint.query_endpoint import router as query_router
from backend.Api_endpoint.get_endpoint import router as get_router
from backend.Api_endpoint.upload_endpoint import router as upload_router

router = APIRouter()

router.include_router(query_router,prefix="/api/v1/query",tags=["Query"])
router.include_router(get_router,prefix="/api/v1/status",tags=["Status"])
router.include_router(upload_router,prefix="/api/v1/upload",tags=["Upload"])
