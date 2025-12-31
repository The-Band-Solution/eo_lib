from eo_lib.config import Config

from eo_lib.infrastructure.repositories import (
    PostgresPersonRepository,
    PostgresTeamRepository,
    PostgresProjectRepository,
    InMemoryPersonRepository,
    InMemoryTeamRepository,
    InMemoryProjectRepository,
    JsonPersonRepository,
    JsonTeamRepository,
    JsonProjectRepository,
)

from eo_lib.services import PersonService, TeamService, ProjectService

class ServiceFactory:
    """
    Factory for creating Service instances with the appropriate Repository Strategy.
    
    The factory determines which storage strategy (Postgres, Memory, or JSON) 
    to use based on the application configuration and injects the corresponding 
    repository into the created services.
    """
    
    @staticmethod
    def _get_strategies():
        """
        Determines the repository classes based on the configured storage type.
        
        Returns:
            tuple: A tuple containing (PersonRepoClass, TeamRepoClass, ProjectRepoClass).
        """
        t = Config.get_storage_type().lower()
        if t == 'memory':
            return InMemoryPersonRepository, InMemoryTeamRepository, InMemoryProjectRepository
        elif t == 'json':
            return JsonPersonRepository, JsonTeamRepository, JsonProjectRepository
        else: # default to db/postgres
            return PostgresPersonRepository, PostgresTeamRepository, PostgresProjectRepository

    @staticmethod
    def create_person_service() -> PersonService:
        """
        Creates and returns a PersonService instance.
        
        Returns:
            PersonService: Initialized with the configured repository strategy.
        """
        RepoClass, _, _ = ServiceFactory._get_strategies()
        return PersonService(RepoClass())

    @staticmethod
    def create_team_service() -> TeamService:
        """
        Creates and returns a TeamService instance.
        
        Returns:
            TeamService: Initialized with the configured repository strategy.
        """
        _, RepoClass, _ = ServiceFactory._get_strategies()
        return TeamService(RepoClass())

    @staticmethod
    def create_project_service() -> ProjectService:
        """
        Creates and returns a ProjectService instance.
        
        Returns:
            ProjectService: Initialized with the configured repository strategy.
        """
        _, _, RepoClass = ServiceFactory._get_strategies()
        return ProjectService(RepoClass())
