from eo_lib.infrastructure.database.postgres_client import PostgresClient
from libbase.infrastructure.sql_repository import GenericSqlRepository
from eo_lib.domain.entities.initiative import Initiative
from eo_lib.domain.repositories.initiative_repository import InitiativeRepository


class PostgresInitiativeRepository(
    GenericSqlRepository[Initiative], InitiativeRepository
):
    """
    PostgreSQL implementation of the Initiative Repository.
    """

    def __init__(self):
        """Initializes the repository by getting a session from PostgresClient."""
        client = PostgresClient()
        super().__init__(client.get_session(), Initiative)
