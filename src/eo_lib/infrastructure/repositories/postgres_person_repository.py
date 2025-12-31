from eo_lib.domain.entities import Person
from eo_lib.domain.repositories import PersonRepositoryInterface
from libbase.infrastructure.sql_repository import GenericSqlRepository

from eo_lib.infrastructure.database.postgres_client import PostgresClient


class PostgresPersonRepository(GenericSqlRepository[Person], PersonRepositoryInterface):
    """
    PostgreSQL implementation of the Person Repository.
    """

    def __init__(self):
        """Initializes the repository by getting a session from PostgresClient."""
        client = PostgresClient()
        super().__init__(client.get_session(), Person)
