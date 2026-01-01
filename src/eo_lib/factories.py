from eo_lib.config import Config

from eo_lib.infrastructure.repositories import (
    PostgresPersonRepository,
    PostgresTeamRepository,
    PostgresInitiativeRepository,
    PostgresInitiativeTypeRepository,
    PostgresOrganizationRepository,
    PostgresOrganizationalUnitRepository,
    InMemoryPersonRepository,
    InMemoryTeamRepository,
    InMemoryInitiativeRepository,
    InMemoryInitiativeTypeRepository,
    InMemoryOrganizationRepository,
    InMemoryOrgUnitRepository,
    JsonPersonRepository,
    JsonTeamRepository,
    JsonInitiativeRepository,
    JsonInitiativeTypeRepository,
    JsonOrganizationRepository,
    JsonOrgUnitRepository,
)

from eo_lib.services import (
    PersonService,
    TeamService,
    InitiativeService,
    OrganizationService,
    OrganizationalUnitService,
)


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
            tuple: (PersonRepo, TeamRepo, InitiativeRepo, InitiativeTypeRepo, OrganizationRepo, OrgUnitRepo)
        """
        t = Config.get_storage_type().lower()
        if t == "memory":
            return (
                InMemoryPersonRepository,
                InMemoryTeamRepository,
                InMemoryInitiativeRepository,
                InMemoryInitiativeTypeRepository,
                InMemoryOrganizationRepository,
                InMemoryOrgUnitRepository,
            )
        elif t == "json":
            return (
                JsonPersonRepository,
                JsonTeamRepository,
                JsonInitiativeRepository,
                JsonInitiativeTypeRepository,
                JsonOrganizationRepository,
                JsonOrgUnitRepository,
            )
        else:  # default to db/postgres
            return (
                PostgresPersonRepository,
                PostgresTeamRepository,
                PostgresInitiativeRepository,
                PostgresInitiativeTypeRepository,
                PostgresOrganizationRepository,
                PostgresOrganizationalUnitRepository,
            )

    @staticmethod
    def create_person_service() -> PersonService:
        RepoClass, _, _, _, _, _ = ServiceFactory._get_strategies()
        return PersonService(RepoClass())

    @staticmethod
    def create_team_service() -> TeamService:
        _, RepoClass, _, _, _, _ = ServiceFactory._get_strategies()
        return TeamService(RepoClass())

    @staticmethod
    def create_initiative_service() -> InitiativeService:
        _, TeamRepoClass, InitiativeRepoClass, InitiativeTypeRepoClass, _, _ = (
            ServiceFactory._get_strategies()
        )
        return InitiativeService(
            InitiativeRepoClass(), InitiativeTypeRepoClass(), TeamRepoClass()
        )

    @staticmethod
    def create_organization_service() -> OrganizationService:
        _, _, _, _, RepoClass, _ = ServiceFactory._get_strategies()
        return OrganizationService(RepoClass())

    @staticmethod
    def create_organizational_unit_service() -> OrganizationalUnitService:
        _, _, _, _, _, RepoClass = ServiceFactory._get_strategies()
        return OrganizationalUnitService(RepoClass())
