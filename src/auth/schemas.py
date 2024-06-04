from typing import Optional

from pydantic import BaseModel


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    kind: str
    localId: str
    email: str
    displayName: str
    idToken: str
    registered: bool
    refreshToken: str
    expiresIn: int


class AuthResponse(BaseModel):
    payload: Optional[LoginResponse] = None
    description: str
    status: int
