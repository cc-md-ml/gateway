import json

from fastapi import status
from fastapi import HTTPException

from firebase_admin import (
    auth,
    exceptions as authx,
)
import httpx

from src.config import (
    setup_env, get_env_value
)

from src.auth.schemas import (
    RegisterRequest, LoginRequest,
    AuthResponse, LoginResponse
)


setup_env()


class AuthService():
    """
    Authentication service class for login, register, and user management.
    """
    def __init__(self):
        self.API_KEY = get_env_value('FIREBASE_WEB_API_KEY')

    def register(self, body: RegisterRequest) -> AuthResponse:
        """
        Creates user with corresponding email and password.
        """
        user: auth.UserRecord
        try:
            user = auth.create_user(
                email=body.email,
                password=body.password
            )
        # invalid user properties
        except ValueError:
            return AuthResponse(
                description="Invalid user properties.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        # error while creating user
        except authx.FirebaseError:
            return AuthResponse(
                description="Error while creating user or user could already exist.",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        else:
            return AuthResponse(
                description=f"Succesfully registered user with email {user.email}.",
                status=status.HTTP_201_CREATED,
            )
         
    async def login(self, body: LoginRequest) -> LoginResponse:
        """
        Authenticates user through email and firebase.
        """
        user: auth.UserRecord
        try:
            # check if email exists
            user = auth.get_user_by_email(body.email)
            headers = { 'Content-Type': 'application/json' }
            data = {
                    'email': body.email,
                    'password': body.password,
                    'returnSecureToken': 'true'
            }
            response = httpx.post(
                url=f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}',
                headers=headers,
                data=json.dumps(data)
            )
        # if credentials mismatch
        except HTTPException as ex:
            return AuthResponse(
                description=ex.detail,
                status=ex.status_code,
            )
        # if email malformed, empty, or None
        except ValueError:
            return AuthResponse(
                description="Request malformed.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        # if user by email does not exists
        except auth.UserNotFoundError as ex:
            return AuthResponse(
                description=ex.default_message,
                status=status.HTTP_401_UNAUTHORIZED,
            )
        # error while retrieving user
        except authx.FirebaseError:
            return AuthResponse(
                description="Error while retrieving user details.",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        else:
            # load json response into dict, map to  LoginResponse schema for payload
            response_body = json.loads(response.content.decode('utf-8'))
            payload = LoginResponse(
                kind=response_body['kind'],
                localId=response_body['localId'],
                email=response_body['email'],
                displayName=response_body['displayName'],
                idToken=response_body['idToken'],
                registered=response_body['registered'],
                refreshToken=response_body['refreshToken'],
                expiresIn=response_body['expiresIn'],
            )
            return AuthResponse(
                payload=payload,
                description=f"User with email {user.email} successfully logged in.",
                status=status.HTTP_200_OK,
            )
        