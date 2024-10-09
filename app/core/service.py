from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, Optional, Type, TypeAlias, TypeVar, cast

from httpx import delete
from pydantic import UUID4, BaseModel

from app.core.repository import AbstractRepository
from app.core.transaction_manager import ITransactionManager

from app.core.exceptions import IncorrectIdException, MissingRepositoryError, UnauthorizedAccessException
from app.users.models import User
from app.users.schemas import UserUpdate


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

    @property
    @abstractmethod
    def repository(self) -> AbstractRepository:
        """Property to access the repository associated with the entity."""
        pass

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
    
    
class AbstractServiceWithUser(ABC, Generic[T]):
    """
    Abstract base class for service layer classes that require user context.
    Provides the interface for user-dependent CRUD operations and manages the repository
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

    @property
    @abstractmethod
    def repository(self) -> AbstractRepository:
        """Property to access the repository associated with the entity."""
        pass

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

    Attributes:
    - entity_type (Type[T]): The type of the entity being managed by the service.
    - transaction_manager (ITransactionManager): Manages database transactions.
    - user_manager (UserManager): Handles user-related operations and authentication.
    - _repository (AbstractRepository): Repository instance for the entity, lazily initialized.
    """
    def __init__(
        self,
        entity_type: Type[T],
        transaction_manager: ITransactionManager,
        user_manager: "UserManager",
    ):
        self.entity_type = entity_type
        self.transaction_manager = transaction_manager
        self._repository: Optional[AbstractRepository] = None
        self.user_manager = user_manager

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

    async def get_all(self) -> list[T] | None:
        async with self.transaction_manager:
            return await self.repository.find_all()

    async def get_by_id(self, entity_id) -> T | None:
        async with self.transaction_manager:
            entity = await self.repository.find_one_or_none(id=entity_id)
            if not entity:
                raise IncorrectIdException(f"Incorrect {self.entity_type.__name__} id")
            return entity

    async def create(self, entity: T) -> T:
        async with self.transaction_manager:
            created_entity = await self.repository.insert_data(**entity.model_dump())
            return cast(T, created_entity)

    async def delete(self, entity_id: int) -> int:
        async with self.transaction_manager:
            deleted_count = await self.repository.delete(id=entity_id)
            return cast(int, deleted_count)

    async def update(self, entity_id, **data) -> int:
        async with self.transaction_manager:
            updated_count = await self.repository.update_fields_by_id(entity_id, **data)
            return cast(int, updated_count)
