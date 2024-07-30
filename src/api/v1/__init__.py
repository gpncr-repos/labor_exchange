from fastapi import APIRouter

from api.v1.users.routers import router as user_router
from api.v1.auth.routers import router as auth_router

router = APIRouter(prefix="/v1")
router.include_router(auth_router)
router.include_router(user_router)
