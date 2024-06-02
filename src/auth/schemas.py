from typing import Optional

from pydantic import BaseModel


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str


class AuthResponse(BaseModel):
    payload: Optional[LoginResponse] = None
    description: str
    status: int
