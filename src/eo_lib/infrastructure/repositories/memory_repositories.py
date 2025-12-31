from typing import List, Optional, TypeVar, Generic
from eo_lib.domain.repositories import (
    GenericRepositoryInterface,
    PersonRepositoryInterface,
    TeamRepositoryInterface,
    ProjectRepositoryInterface,
)
from eo_lib.domain.entities import Person, Team, TeamMember, Project

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


class InMemoryProjectRepository(
    GenericMemoryRepository[Project], ProjectRepositoryInterface
):
    """
    In-Memory implementation of the Project Repository.
    """

    def __init__(self):
        """Initializes the project repository and team assignment store."""
        super().__init__(Project)
        # Simplified handling for Many-to-Many in memory without full ORM simulation
        self._proj_teams = {}

    def add_team_to_project(self, project_id: int, team_id: int) -> None:
        """
        Assigns a team to a project in memory.

        Args:
            project_id (int): ID of the project.
            team_id (int): ID of the team to assign.
        """
        if project_id not in self._proj_teams:
            self._proj_teams[project_id] = []
        self._proj_teams[project_id].append(team_id)

    def get_teams(self, project_id: int) -> List[Team]:
        """
        Retrieves assigned teams. (Note: Current limited implementation returns empty).

        Args:
            project_id (int): ID of the project.

        Returns:
            List[Team]: Empty list (current limitation).
        """
        # Limitations of simple memory repo: cannot easily join with TeamRepo
        return []
