from typing import Type, TypeVar, List, Optional, Generic
from eo_lib.domain.repositories.generic_repository import GenericRepositoryInterface
from eo_lib.infrastructure.database.postgres_client import PostgresClient

T = TypeVar('T')

class GenericPostgresRepository(GenericRepositoryInterface[T]):
    """
    Generic PostgreSQL Repository implementation using SQLAlchemy.
    
    Provides a base implementation for standard CRUD operations that interacts
    with a PostgreSQL database using provided SQLAlchemy entities.
    """
    def __init__(self, model_cls: Type[T]):
        """
        Initializes the repository for a specific model class.
        
        Args:
            model_cls (Type[T]): The SQLAlchemy declarative class this repository handles.
        """
        self.client = PostgresClient()
        self.model_cls = model_cls

    def add(self, entity: T) -> T:
        """
        Adds a new entity to the database.
        
        Args:
            entity (T): The entity instance to persist.
            
        Returns:
            T: The persisted entity instance with updated state (e.g., generated ID).
        """
        session = self.client.get_session()
        try:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity
        finally:
            session.close()

    def get(self, id: int) -> Optional[T]:
        """
        Retrieves an entity by its primary key ID.
        
        Args:
            id (int): The unique identifier of the entity.
            
        Returns:
            Optional[T]: The entity if found, otherwise None.
        """
        session = self.client.get_session()
        try:
            return session.query(self.model_cls).filter_by(id=id).first()
        finally:
            session.close()

    def update(self, entity: T) -> T:
        """
        Updates an existing entity record using merge.
        
        Args:
            entity (T): The entity instance containing updated values.
            
        Returns:
            T: The updated and persistent entity instance.
        """
        session = self.client.get_session()
        try:
            # updated_entity = session.merge(entity) 
            updated_entity = session.merge(entity) 
            session.commit()
            return updated_entity
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def delete(self, id: int) -> bool:
        """
        Deletes an entity record by its ID.
        
        Args:
            id (int): The ID of the entity to delete.
            
        Returns:
            bool: True if the entity was deleted, False if not found.
        """
        session = self.client.get_session()
        try:
            obj = session.query(self.model_cls).filter_by(id=id).first()
            if obj:
                session.delete(obj)
                session.commit()
                return True
            return False
        finally:
            session.close()

    def list(self) -> List[T]:
        """
        Retrieves all records for the handled model class.
        
        Returns:
            List[T]: A list of all entities found.
        """
        session = self.client.get_session()
        try:
            return session.query(self.model_cls).all()
        finally:
            session.close()
