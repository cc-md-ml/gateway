from fastapi import (
    APIRouter, Response
)

from src.auth.service import AuthService
from src.auth.schemas import (
    RegisterRequest, LoginRequest,
    AuthResponse
)


SERVICE = AuthService()


router = APIRouter(
    prefix="/auth",
    responses={ 
        404: { "message": "Not found" } 
    },
)


@router.post(
    "/register",
    responses={
        400: { "description": "Invalid registration credentials." },
    }
)
async def register(body: RegisterRequest) -> Response:
    # TODO: implement register service
    res: AuthResponse = SERVICE.register(body)
    return Response(
        content=res.description,
        status_code=res.status,
    )


@router.post(
    "/login",
    responses={ 
        401: { "description": "Invalid username or password." },
    },
)
async def login(body: LoginRequest) -> Response:
    # TODO: implement login service
    res = SERVICE.login(body)
    return Response(
        content=res.description,
        status_code=res.status,
    )

