from typing import List, Optional, TypeVar, Generic
from eo_lib.domain.repositories.generic_repository import GenericRepositoryInterface
from eo_lib.domain.entities.person import Person
from eo_lib.domain.repositories.person_repository import PersonRepositoryInterface
from eo_lib.domain.entities.team import Team, TeamMember
from eo_lib.domain.repositories.team_repository import TeamRepositoryInterface
from eo_lib.domain.entities.project import Project
from eo_lib.domain.repositories.project_repository import ProjectRepositoryInterface

T = TypeVar('T')

class GenericMemoryRepository(GenericRepositoryInterface[T]):
    """
    Generic In-Memory Repository.
    """
    def __init__(self):
        self._store = {}
        self._id_counter = 1

    def add(self, entity: T) -> T:
        entity.id = self._id_counter
        self._store[entity.id] = entity
        self._id_counter += 1
        return entity

    def get(self, id: int) -> Optional[T]:
        return self._store.get(id)

    def update(self, entity: T) -> T:
        if hasattr(entity, 'id') and entity.id in self._store:
            self._store[entity.id] = entity
            return entity
        raise ValueError(f"Entity {getattr(entity, 'id', '?')} not found")

    def delete(self, id: int) -> bool:
        if id in self._store:
            del self._store[id]
            return True
        return False

    def list(self) -> List[T]:
        return list(self._store.values())

class InMemoryPersonRepository(GenericMemoryRepository[Person], PersonRepositoryInterface):
    """Memory Strategy for Person."""
    pass

class InMemoryTeamRepository(GenericMemoryRepository[Team], TeamRepositoryInterface):
    """Memory Strategy for Team."""
    def __init__(self):
        super().__init__()
        self._members = {}
        self._member_id_counter = 1

    def add_member(self, member: TeamMember) -> TeamMember:
        member.id = self._member_id_counter
        self._members[member.id] = member
        self._member_id_counter += 1
        return member

    def remove_member(self, member_id: int) -> bool:
        if member_id in self._members:
            del self._members[member_id]
            return True
        return False

    def get_members(self, team_id: int) -> List[TeamMember]:
        return [m for m in self._members.values() if m.team_id == team_id]

class InMemoryProjectRepository(GenericMemoryRepository[Project], ProjectRepositoryInterface):
    """Memory Strategy for Project."""
    def __init__(self):
        super().__init__()
        # Simplified handling for Many-to-Many in memory without full ORM simulation
        self._proj_teams = {} 

    def add_team_to_project(self, project_id: int, team_id: int) -> None:
        if project_id not in self._proj_teams:
            self._proj_teams[project_id] = []
        self._proj_teams[project_id].append(team_id)

    def get_teams(self, project_id: int) -> List[Team]:
        # Limitations of simple memory repo: cannot easily join with TeamRepo
        return []
