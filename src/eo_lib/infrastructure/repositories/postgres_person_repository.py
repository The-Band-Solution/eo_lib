from eo_lib.domain.entities.person import Person
from eo_lib.domain.repositories.person_repository import PersonRepositoryInterface
from eo_lib.infrastructure.repositories.generic_postgres_repository import GenericPostgresRepository

class PostgresPersonRepository(GenericPostgresRepository[Person], PersonRepositoryInterface):
    """
    Repository for Person entity using PostgreSQL.
    """
    def __init__(self):
        super().__init__(Person)
