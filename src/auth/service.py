from fastapi import status
from fastapi import HTTPException

from firebase_admin import (
    auth,
    exceptions as authx,
)

from src.auth.schemas import (
    RegisterRequest, LoginRequest,
    AuthResponse, LoginResponse
)


class AuthService():
    """
    Authentication service class for login, register, and user management.
    """
    def __init__(self):
        pass

    def register(self, body: RegisterRequest) -> AuthResponse:
        """
        Creates user with corresponding email and password.
        """
        user: auth.UserRecord
        try:
            user = auth.create_user(email=body.email)
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
         
    def login(self, body: LoginRequest) -> LoginResponse:
        """
        Authenticates user through email and firebase.
        """
        user: auth.UserRecord
        try:
            user = auth.get_user_by_email(body.email)
            if user.password != body.password:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password."
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
            token = auth.create_custom_token(
                uid=user.uid,
                developer_claims={
                    "email": user.email,
                }
            )
            response = LoginResponse(token=token)
            return AuthResponse(
                payload=response,
                description=f"User with email {user.email} successfully logged in.",
                status=status.HTTP_200_OK,
            )
        