from typing import Optional
from eo_lib.infrastructure.database.postgres_client import PostgresClient
from libbase.infrastructure.sql_repository import GenericSqlRepository
from eo_lib.domain.entities.initiative import InitiativeType
from eo_lib.domain.repositories.initiative_type_repository import (
    InitiativeTypeRepository,
)


class PostgresInitiativeTypeRepository(
    GenericSqlRepository[InitiativeType], InitiativeTypeRepository
):
    """
    PostgreSQL implementation of the InitiativeType Repository.
    """

    def __init__(self):
        """Initializes the repository by getting a session from PostgresClient."""
        client = PostgresClient()
        super().__init__(client.get_session(), InitiativeType)

    def get_by_name(self, name: str) -> Optional[InitiativeType]:
        return (
            self.session.query(InitiativeType)
            .filter(InitiativeType.name == name)
            .first()
        )
