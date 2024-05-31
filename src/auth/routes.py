from fastapi import APIRouter

from .schemas import (
    RegisterRequest, LoginRequest
)


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
    return body.model_dump(mode='json')


@router.post(
    "/login",
    responses={ 
        401: { "description": "Invalid username or password." },
    },
)
async def login(body: LoginRequest):
    # TODO: implement login service
    return body.model_dump(mode='json')
