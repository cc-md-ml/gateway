import os

from fastapi import (
    Depends, 
    HTTPException, status, Response
)
from fastapi.security import (
    HTTPBearer, HTTPAuthorizationCredentials
)

from firebase_admin import (
    auth, credentials, 
    initialize_app
)


def init_auth() -> None:
    """
    Initializes firebase authentication with service account credentials.
    """
    credential = credentials.Certificate(f'{os.getcwd()}/service_account_key.json')
    initialize_app(credential)


def get_user_token(
        res: Response, 
        credential: HTTPAuthorizationCredentials=Depends(HTTPBearer(auto_error=False))
    ):
    """
    Middleware to verify if requests is from authorized/authenticated user.
    """
    if credential is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication is needed",
            headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
        )
    try:
        decoded_token = auth.verify_id_token(credential.credentials)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication from Firebase. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )
    res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
    return decoded_token