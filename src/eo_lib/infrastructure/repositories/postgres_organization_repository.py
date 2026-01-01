from eo_lib.domain.entities import Organization
from eo_lib.domain.repositories import OrganizationRepositoryInterface
from libbase.infrastructure.sql_repository import GenericSqlRepository
from eo_lib.infrastructure.database.postgres_client import PostgresClient


class PostgresOrganizationRepository(
    GenericSqlRepository[Organization], OrganizationRepositoryInterface
):
    """
    PostgreSQL implementation of the Organization Repository.
    """

    def __init__(self):
        """Initializes the repository by getting a session from PostgresClient."""
        client = PostgresClient()
        super().__init__(client.get_session(), Organization)
