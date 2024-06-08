from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.auth.service import AuthService
from src.auth.schemas import (
    RegisterRequest, LoginRequest, AuthResponse,
    TokenRequest, TokenResponse
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
    return jsonable_encoder(res)


@router.post(
    "/login",
    responses={ 
        401: { "description": "Invalid username or password." },
    },
)
async def login(body: LoginRequest) -> JSONResponse:
    res: AuthResponse = await service.login(body)
    return jsonable_encoder(res)


@router.post(
    "/refresh-token",
    responses={
        401: { "description": "Token has expired." } 
    },
    response_model=TokenResponse
)
async def refresh_token(body: TokenRequest) -> JSONResponse:
    res: TokenResponse = await service.refresh_token(body)
    return jsonable_encoder(res)