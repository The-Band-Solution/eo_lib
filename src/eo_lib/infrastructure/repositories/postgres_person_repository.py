from eo_lib.domain.entities import Person
from eo_lib.domain.repositories import PersonRepositoryInterface
from eo_lib.infrastructure.repositories.generic_postgres_repository import GenericPostgresRepository

class PostgresPersonRepository(GenericPostgresRepository[Person], PersonRepositoryInterface):
    """
    PostgreSQL implementation of the Person Repository.
    
    Inherits generic CRUD operations from GenericPostgresRepository and
    implements the PersonRepositoryInterface contract.
    """
    def __init__(self):
        """Initializes the repository with the Person model."""
        super().__init__(Person)
