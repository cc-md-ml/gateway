from fastapi import APIRouter

from src.auth.service import AuthService
from src.auth.schemas import (
    RegisterRequest, LoginRequest
)


SERVICE = AuthService()


router = APIRouter(
    prefix="/auth",
    responses={ 404: { 
        "message": "Not found" } 
    },
)


@router.post(
    "/register",
    responses={
        400: { "description": "Invalid registration credentials." },
    }
)
async def register(body: RegisterRequest):
  # TODO: implement register service
    res = SERVICE.register()
    return res


@router.post(
    "/login",
    responses={ 
        401: { "description": "Invalid username or password." },
    },
)
async def login(body: LoginRequest):
    # TODO: implement login service
    res = SERVICE.login()
    return res

