from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.auth.service import AuthService
from src.auth.schemas import (
    AuthResponse,
    RegisterRequest, 
    LoginRequest, LoginResponse, 
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
    response_model=AuthResponse, 
    description="**For example response values:** [Click Here](https://firebase.google.com/docs/reference/rest/auth)",
    
)
async def register(body: RegisterRequest) -> JSONResponse:
    res: AuthResponse = await service.register(body)
    return jsonable_encoder(res)


@router.post(
    "/login",
    response_model=LoginResponse,
    description="**For example response values:** [Click Here](https://firebase.google.com/docs/reference/rest/auth)",
)
async def login(body: LoginRequest) -> JSONResponse:
    res: LoginResponse = await service.login(body)
    return jsonable_encoder(res)


@router.post(
    "/refresh-token",
    response_model=TokenResponse,
    description="""
    **For example response values:** [Click Here](https://firebase.google.com/docs/reference/rest/auth)

`grant_type` field should always be `refresh_token`.
    """,
)
async def refresh_token(body: TokenRequest) -> JSONResponse:
    res: TokenResponse = await service.refresh_token(body)
    return jsonable_encoder(res)
