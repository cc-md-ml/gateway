from typing import Any

from fastapi import HTTPException, status


class GlobalHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Server error."

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class ImproperlyConfigured(Exception):
    DETAIL = "Environment variables are improperly configured."
