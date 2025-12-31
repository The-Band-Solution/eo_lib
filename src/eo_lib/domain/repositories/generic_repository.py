from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional

T = TypeVar('T')

class GenericRepositoryInterface(ABC, Generic[T]):
    """
    Abstract Base Class for Generic Repository.
    
    Defines the standard set of CRUD (Create, Read, Update, Delete) operations
    that all repository implementations must support for a given entity type T.
    """

    @abstractmethod
    def add(self, entity: T) -> T:
        """
        Adds a new entity to the persistence storage.
        
        Args:
            entity (T): The entity instance to be stored.
            
        Returns:
            T: The stored entity (often updated with a generated ID).
        """
        pass

    @abstractmethod
    def get(self, id: int) -> Optional[T]:
        """
        Retrieves a single entity by its unique identifier.
        
        Args:
            id (int): The unique identifier of the entity.
            
        Returns:
            Optional[T]: The entity if found, otherwise None.
        """
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """
        Updates an existing entity in the persistence storage.
        
        Args:
            entity (T): The entity instance with updated values.
            
        Returns:
            T: The updated entity.
        """
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        """
        Removes an entity from the persistence storage.
        
        Args:
            id (int): The unique identifier of the entity to be deleted.
            
        Returns:
            bool: True if the entity was successfully deleted, False otherwise.
        """
        pass

    @abstractmethod
    def list(self) -> List[T]:
        """
        Retrieves all entities of type T from the persistence storage.
        
        Returns:
            List[T]: A list containing all retrieved entities.
        """
        pass
