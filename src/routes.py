from fastapi import APIRouter

from src.auth.routes import router as auth_router
from src.langchain.routes import router as llm_router
# from src.classification.routes import router as classification_router


global_router = APIRouter()

global_router.include_router(auth_router, tags=["Authentication"])
# global_router.include_router(classification_router, tags=["Classification"])
global_router.include_router(llm_router, tags=["LangChain"])
