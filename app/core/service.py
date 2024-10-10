from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, Optional, Type, TypeVar, cast, final

from pydantic import BaseModel

from app.core.repository import AbstractRepository
from app.core.transaction_manager import ITransactionManager
from app.core.exceptions import IncorrectIdException, MissingRepositoryError
from app.users.models import User


if TYPE_CHECKING:
    from app.users.manager import UserManager

T = TypeVar("T", bound=BaseModel)


class AbstractService(ABC, Generic[T]):
    """
    Abstract base class for service layer classes.
    Provides the interface for CRUD operations and manages the repository
    interactions through a transaction manager.
    """

    def __init__(
        self,
        entity_type: Type[T],
        transaction_manager: "ITransactionManager",
        user_manager: "UserManager",
    ):
        self.entity_type = entity_type
        self.transaction_manager = transaction_manager
        self.user_manager = user_manager
        self._repository: Optional[AbstractRepository] = None

    @final
    @property
    def repository(self) -> AbstractRepository:
        if self._repository is None:
            try:
                self._repository = getattr(
                    self.transaction_manager, self.entity_type.__name__.lower()
                )
            except AttributeError as e:
                raise MissingRepositoryError(self.entity_type.__name__.lower()) from e
        return cast(AbstractRepository, self._repository)

    @abstractmethod
    async def get_all(self) -> list[T] | None:
        """Fetch all entities from the repository."""
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> T | None:
        """Fetch a single entity by its ID."""
        pass

    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create a new entity in the repository."""
        pass

    @abstractmethod
    async def delete(self, entity_id: int) -> int:
        """Delete an entity by its ID."""
        pass

    @abstractmethod
    async def update(self, entity_id: int, **data) -> int:
        """Update fields of an entity by its ID."""
        pass
    
    
class AbstractServiceWithUser(AbstractService, Generic[T]):
    """
    Abstract base class for service layer classes that require user context.
    Provides the interface for user-dependent CRUD operations and manages the repository
    interactions through a transaction manager.
    """

    @abstractmethod
    async def get_all(self, user: User) -> list[T] | None:
        """
        Fetch all entities from the repository for the specified user.
        
        Args:
            user (User): The user for whom to fetch entities.

        Returns:
            list[T] | None: A list of entities or None if not found.
        """
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: int, user: User) -> T | None:
        """
        Fetch a single entity by its ID for the specified user.
        
        Args:
            entity_id (int): The ID of the entity to fetch.
            user (User): The user for whom to fetch the entity.

        Returns:
            T | None: The entity or None if not found.
        """
        pass

    @abstractmethod
    async def create(self, entity: T, user: User) -> T:
        """
        Create a new entity in the repository for the specified user.
        
        Args:
            entity (T): The entity data to create.
            user (User): The user creating the entity.

        Returns:
            T: The created entity.
        """
        pass

    @abstractmethod
    async def delete(self, entity_id: int, user: User) -> int:
        """
        Delete an entity by its ID for the specified user.
        
        Args:
            entity_id (int): The ID of the entity to delete.
            user (User): The user attempting the deletion.

        Returns:
            int: The number of deleted entities (0 or 1).
        """
        pass

    @abstractmethod
    async def update(self, entity_id: int, user: User, **data) -> int:
        """
        Update fields of an entity by its ID for the specified user.
        
        Args:
            entity_id (int): The ID of the entity to update.
            user (User): The user making the update.
            **data: The fields to update in the entity.

        Returns:
            int: The number of updated entities (0 or 1).
        """
        pass


class BaseService(AbstractService, Generic[T]):
    """
    Base service class providing common CRUD operations for a given entity type.
    Manages interaction with the repository and ensures operations are wrapped
    in a transaction.
    """

    async def get_all(self) -> list[T] | None:
        async with self.transaction_manager:
            return await self.repository.find_all()

    async def get_by_id(self, entity_id) -> T | None:
        async with self.transaction_manager:
            entity = await self.repository.find_one_or_none(id=entity_id)
            if not entity:
                raise IncorrectIdException(f"Incorrect {self.entity_type.__name__} id")
            return entity

    async def create(self, entity: T) -> T | None:
        async with self.transaction_manager:
            return await self.repository.insert_data(**entity.model_dump())

    async def delete(self, entity_id: int) -> int | None:
        async with self.transaction_manager:
            return await self.repository.delete(id=entity_id)

    async def update(self, entity_id, **data) -> int | None:
        async with self.transaction_manager:
            return await self.repository.update_fields_by_id(entity_id, **data)
