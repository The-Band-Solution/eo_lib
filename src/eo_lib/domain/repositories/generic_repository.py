from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional

T = TypeVar('T')

class GenericRepositoryInterface(ABC, Generic[T]):
    """
    Abstract Base Class for Generic Repository.
    Defines standard CRUD operations for entity T.
    """

    @abstractmethod
    def add(self, entity: T) -> T:
        """Add a new entity."""
        pass

    @abstractmethod
    def get(self, id: int) -> Optional[T]:
        """Get entity by ID."""
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an entity."""
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        """Delete entity by ID."""
        pass

    @abstractmethod
    def list(self) -> List[T]:
        """List all entities."""
        pass
