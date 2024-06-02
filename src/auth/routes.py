from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.auth.service import AuthService
from src.auth.schemas import (
    RegisterRequest, LoginRequest,
    AuthResponse, LoginResponse
)


service = AuthService()
router = APIRouter(
    prefix="/auth",
    responses={ 
        404: { "description": "Not found" } 
    },
)


@router.post(
    "/register",
    responses={
        400: { "description": "Invalid registration credentials." },
    }
)
async def register(body: RegisterRequest) -> JSONResponse:
    res: AuthResponse = service.register(body)
    return JSONResponse(
        content=res.description,
        status_code=res.status,
    )


@router.post(
    "/login",
    responses={ 
        401: { "description": "Invalid username or password." },
    },
)
async def login(body: LoginRequest) -> JSONResponse:
    res: AuthResponse = service.login(body)
    return JSONResponse(
        content=res,
        status_code=res.status,
    )
