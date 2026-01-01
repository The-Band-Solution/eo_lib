from typing import List, Optional
from eo_lib.domain.repositories import (
    PersonRepositoryInterface,
    TeamRepositoryInterface,
    InitiativeRepository,
    InitiativeTypeRepository,
    OrganizationRepositoryInterface,
    OrganizationalUnitRepositoryInterface,
)
from eo_lib.domain.entities import (
    Person,
    Team,
    TeamMember,
    Initiative,
    InitiativeType,
    Organization,
    OrganizationalUnit,
)

from libbase.infrastructure.memory_repository import GenericMemoryRepository


class InMemoryPersonRepository(
    GenericMemoryRepository[Person], PersonRepositoryInterface
):
    """
    In-Memory implementation of the Person Repository.
    """

    def __init__(self):
        """Initializes the repository with the Person model."""
        super().__init__(Person)


class InMemoryTeamRepository(GenericMemoryRepository[Team], TeamRepositoryInterface):
    """
    In-Memory implementation of the Team Repository.
    """

    def __init__(self):
        """Initializes the team repository and membership store."""
        super().__init__(Team)
        self._members = {}
        self._member_id_counter = 1

    def add_member(self, member: TeamMember) -> TeamMember:
        """Adds a membership association to the in-memory store."""
        member.id = self._member_id_counter
        self._members[member.id] = member
        self._member_id_counter += 1
        return member

    def remove_member(self, member_id: int) -> bool:
        """Removes a membership association from the in-memory store."""
        if member_id in self._members:
            del self._members[member_id]
            return True
        return False

    def get_members(self, team_id: int) -> List[TeamMember]:
        """Retrieves all members of a specific team from the in-memory store."""
        return [m for m in self._members.values() if m.team_id == team_id]


class InMemoryInitiativeRepository(
    GenericMemoryRepository[Initiative], InitiativeRepository
):
    """
    In-Memory implementation of the Initiative Repository.
    """

    def __init__(self):
        """Initializes the initiative repository."""
        super().__init__(Initiative)


class InMemoryInitiativeTypeRepository(
    GenericMemoryRepository[InitiativeType], InitiativeTypeRepository
):
    """
    In-Memory implementation of the Initiative Type Repository.
    """

    def __init__(self):
        """Initializes the initiative type repository."""
        super().__init__(InitiativeType)

    def get_by_name(self, name: str) -> Optional[InitiativeType]:
        return next((t for t in self._storage.values() if t.name == name), None)


class InMemoryOrganizationRepository(
    GenericMemoryRepository[Organization], OrganizationRepositoryInterface
):
    """
    In-Memory implementation of the Organization Repository.
    """

    def __init__(self):
        super().__init__(Organization)


class InMemoryOrgUnitRepository(
    GenericMemoryRepository[OrganizationalUnit], OrganizationalUnitRepositoryInterface
):
    """
    In-Memory implementation of the Organizational Unit Repository.
    """

    def __init__(self):
        super().__init__(OrganizationalUnit)
