from typing import Optional

from pydantic import BaseModel


class AuthRequest(BaseModel):
    email: str = "user@example.com"
    password: str = "String1234"

class RegisterRequest(AuthRequest):
    name: str


class LoginRequest(AuthRequest):
    pass


class LoginBody(BaseModel):
    kind: str
    localId: str
    email: str
    displayName: str
    idToken: str
    registered: bool
    refreshToken: str
    expiresIn: int


class AuthResponse(BaseModel):
    description: str
    status: int


class LoginResponse(AuthResponse):
    payload: Optional[LoginBody] = None

class TokenRequest(BaseModel):
    grant_type: str = "refresh_token"   # should always be 'refresh_token'
    refresh_token: str

class TokenResponse(BaseModel):
    expires_in: int = 3600
    token_type: str = "Bearer"
    refresh_token: str
    id_token: str
    user_id: str
    project_id: str
