from fastapi import APIRouter

from .auth.routes import router as auth_router
from .llm.routes import router as llm_router


global_router = APIRouter()

global_router.include_router(auth_router, tags=["Authentication"])
global_router.include_router(llm_router, tags=["llm"])
