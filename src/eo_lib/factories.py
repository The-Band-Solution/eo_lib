from eo_lib.config import Config

# SQL Strategies
from eo_lib.infrastructure.repositories.postgres_person_repository import PostgresPersonRepository
from eo_lib.infrastructure.repositories.postgres_team_repository import PostgresTeamRepository
from eo_lib.infrastructure.repositories.postgres_project_repository import PostgresProjectRepository

# Memory Strategies
from eo_lib.infrastructure.repositories.memory_repositories import InMemoryPersonRepository, InMemoryTeamRepository, InMemoryProjectRepository

# JSON Strategies
from eo_lib.infrastructure.repositories.json_repositories import JsonPersonRepository, JsonTeamRepository, JsonProjectRepository

from eo_lib.services.person_service import PersonService
from eo_lib.services.team_service import TeamService
from eo_lib.services.project_service import ProjectService

class ServiceFactory:
    """
    Factory creating Services with the correct Repository Strategy.
    """
    
    @staticmethod
    def _get_strategies():
        t = Config.get_storage_type().lower()
        if t == 'memory':
            return InMemoryPersonRepository, InMemoryTeamRepository, InMemoryProjectRepository
        elif t == 'json':
            return JsonPersonRepository, JsonTeamRepository, JsonProjectRepository
        else: # default to db/postgres
            return PostgresPersonRepository, PostgresTeamRepository, PostgresProjectRepository

    @staticmethod
    def create_person_service() -> PersonService:
        RepoClass, _, _ = ServiceFactory._get_strategies()
        return PersonService(RepoClass())

    @staticmethod
    def create_team_service() -> TeamService:
        _, RepoClass, _ = ServiceFactory._get_strategies()
        return TeamService(RepoClass())

    @staticmethod
    def create_project_service() -> ProjectService:
        _, _, RepoClass = ServiceFactory._get_strategies()
        return ProjectService(RepoClass())
