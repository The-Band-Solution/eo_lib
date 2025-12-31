from typing import Type, TypeVar, List, Optional, Generic
from eo_lib.domain.repositories.generic_repository import GenericRepositoryInterface
from eo_lib.infrastructure.database.postgres_client import PostgresClient

T = TypeVar('T')

class GenericPostgresRepository(GenericRepositoryInterface[T]):
    """
    Generic PostgreSQL Repository implementation using SQL Alchemy.
    """
    def __init__(self, model_cls: Type[T]):
        self.client = PostgresClient()
        self.model_cls = model_cls

    def add(self, entity: T) -> T:
        session = self.client.get_session()
        try:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity
        finally:
            session.close()

    def get(self, id: int) -> Optional[T]:
        session = self.client.get_session()
        try:
            return session.query(self.model_cls).filter_by(id=id).first()
        finally:
            session.close()

    def update(self, entity: T) -> T:
        session = self.client.get_session()
        try:
            # We assume entity.id is set.
            # In a real generic implementation, we might need to merge or look up by PK.
            # Since our entities are declarative models, we can use session.merge but that might detach/attach differently.
            # Sticking to the previous pattern of fetch-and-update or merge.
            # Using merge is the cleanest generic way if 'entity' is a detached instance with an ID.
            updated_entity = session.merge(entity) 
            session.commit()
            return updated_entity
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def delete(self, id: int) -> bool:
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
        session = self.client.get_session()
        try:
            return session.query(self.model_cls).all()
        finally:
            session.close()
