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


class TokenRequest(BaseModel):
    grant_type: str     # should always be 'refresh_token'
    refresh_token: str

class TokenResponse(BaseModel):
    expires_in: int
    token_type: str
    refresh_token: str
    id_token: str
    user_id: str
    project_id: str
