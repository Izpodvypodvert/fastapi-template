from typing import Any, TypeAlias
from fastapi import HTTPException, status
from pydantic import BaseModel


class MissingRepositoryError(Exception):
    def __init__(self, entity_name: str):
        message = f"В TransactionManager в метод __aenter__ необходимо добавить атрибут '{entity_name}'."
        super().__init__(message)


class OpenAPIDocExtraResponse(BaseModel):
    """Class for extra responses in OpenAPI doc"""

    detail: str


class AppException(HTTPException):
    """Base class for all courses exceptions"""

    def __init__(
        self, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, detail: str = ""
    ):
        super().__init__(status_code=status_code, detail=detail)


class IncorrectIdException(AppException):
    """Exception raised when an entity with a specific ID is not found."""

    def __init__(self, message):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )


class UnauthorizedAccessException(AppException):
    """Exception raised when a user attempts to access an entity without authorization."""

    def __init__(self, message="User is not the author of the entity"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
        )


OpenAPIResponses: TypeAlias = dict[int | str, dict[str, Any]]


DEFAULT_RESPONSES: OpenAPIResponses = {
    401: {
        "description": "Unauthorized - The user is not authenticated",
        "model": OpenAPIDocExtraResponse,
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
    },
    403: {
        "description": "Forbidden - The user does not have permission to access this resource",
        "model": OpenAPIDocExtraResponse,
        "content": {"application/json": {"example": {"detail": "Not enough permissions"}}},
    },
    404: {
        "description": "Not Found - The requested resource could not be found",
        "model": OpenAPIDocExtraResponse,
        "content": {"application/json": {"example": {"detail": "Item not found"}}},
    },
    500: {
        "description": "Internal Server Error",
        "model": OpenAPIDocExtraResponse,
        "content": {"application/json": {"example": {"detail": "An error occurred"}}},
    },
}

ERROR_MESSAGES = {
    "REGISTER_INVALID_PASSWORD": "Пароль не соответствует требованиям.",
    "REGISTER_USER_ALREADY_EXISTS": "Пользователь с таким email уже существует.",
    "OAUTH_NOT_AVAILABLE_EMAIL": "OAuth не предоставляет email.",
    "OAUTH_USER_ALREADY_EXISTS": "Пользователь уже существует через OAuth.",
    "LOGIN_BAD_CREDENTIALS": "Неверные учетные данные. Проверьте логин и пароль.",
    "LOGIN_USER_NOT_VERIFIED": "Пользователь не подтвержден.",
    "RESET_PASSWORD_BAD_TOKEN": "Неверный токен для сброса пароля.",
    "RESET_PASSWORD_INVALID_PASSWORD": "Новый пароль не соответствует требованиям.",
    "VERIFY_USER_BAD_TOKEN": "Неверный токен подтверждения.",
    "VERIFY_USER_ALREADY_VERIFIED": "Пользователь уже подтвержден.",
    "UPDATE_USER_EMAIL_ALREADY_EXISTS": "Пользователь с таким email уже существует.",
    "UPDATE_USER_INVALID_PASSWORD": "Неверный текущий пароль."
}