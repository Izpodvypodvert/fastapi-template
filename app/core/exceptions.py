from fastapi import HTTPException, status


class MissingRepositoryError(Exception):
    def __init__(self, entity_name: str):
        message = f"В TransactionManager в метод __aenter__ необходимо добавить атрибут '{entity_name}'."
        super().__init__(message)


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
