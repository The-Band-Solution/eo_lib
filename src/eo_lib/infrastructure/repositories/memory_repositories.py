from typing import List, Optional, TypeVar, Generic
from eo_lib.domain.repositories import (
    GenericRepositoryInterface,
    PersonRepositoryInterface,
    TeamRepositoryInterface,
    ProjectRepositoryInterface,
)
from eo_lib.domain.entities import Person, Team, TeamMember, Project

T = TypeVar('T')

class GenericMemoryRepository(GenericRepositoryInterface[T]):
    """
    Generic In-Memory Repository implementation.
    
    Provides a fast, non-persistent storage strategy using a dictionary.
    Useful for testing and development environments.
    """
    def __init__(self):
        """Initializes the in-memory store and ID counter."""
        self._store = {}
        self._id_counter = 1

    def add(self, entity: T) -> T:
        """
        Adds a new entity to the in-memory store.
        
        Args:
            entity (T): The entity to store.
            
        Returns:
            T: The stored entity with a assigned ID.
        """
        entity.id = self._id_counter
        self._store[entity.id] = entity
        self._id_counter += 1
        return entity

    def get(self, id: int) -> Optional[T]:
        """
        Retrieves an entity by ID from the in-memory store.
        
        Args:
            id (int): The ID of the entity.
            
        Returns:
            Optional[T]: The entity if found, otherwise None.
        """
        return self._store.get(id)

    def update(self, entity: T) -> T:
        """
        Updates an existing entity in the in-memory store.
        
        Args:
            entity (T): The entity with updated values.
            
        Returns:
            T: The updated entity.
            
        Raises:
            ValueError: If the entity is not found in the store.
        """
        if hasattr(entity, 'id') and entity.id in self._store:
            self._store[entity.id] = entity
            return entity
        raise ValueError(f"Entity {getattr(entity, 'id', '?')} not found")

    def delete(self, id: int) -> bool:
        """
        Removes an entity from the in-memory store.
        
        Args:
            id (int): The ID of the entity to delete.
            
        Returns:
            bool: True if deleted, False if not found.
        """
        if id in self._store:
            del self._store[id]
            return True
        return False

    def list(self) -> List[T]:
        """
        Returns all entities currently in the in-memory store.
        
        Returns:
            List[T]: List of all entities.
        """
        return list(self._store.values())

class InMemoryPersonRepository(GenericMemoryRepository[Person], PersonRepositoryInterface):
    """
    In-Memory implementation of the Person Repository.
    """
    pass

class InMemoryTeamRepository(GenericMemoryRepository[Team], TeamRepositoryInterface):
    """
    In-Memory implementation of the Team Repository.
    """
    def __init__(self):
        """Initializes the team repository and membership store."""
        super().__init__()
        self._members = {}
        self._member_id_counter = 1

    def add_member(self, member: TeamMember) -> TeamMember:
        """
        Adds a membership association to the in-memory store.
        
        Args:
            member (TeamMember): The association to store.
            
        Returns:
            TeamMember: The stored association.
        """
        member.id = self._member_id_counter
        self._members[member.id] = member
        self._member_id_counter += 1
        return member

    def remove_member(self, member_id: int) -> bool:
        """
        Removes a membership association from the in-memory store.
        
        Args:
            member_id (int): ID of the membership to remove.
            
        Returns:
            bool: True if removed, False otherwise.
        """
        if member_id in self._members:
            del self._members[member_id]
            return True
        return False

    def get_members(self, team_id: int) -> List[TeamMember]:
        """
        Retrieves all members of a specific team from the in-memory store.
        
        Args:
            team_id (int): ID of the team.
            
        Returns:
            List[TeamMember]: List of membership entities.
        """
        return [m for m in self._members.values() if m.team_id == team_id]

class InMemoryProjectRepository(GenericMemoryRepository[Project], ProjectRepositoryInterface):
    """
    In-Memory implementation of the Project Repository.
    """
    def __init__(self):
        """Initializes the project repository and team assignment store."""
        super().__init__()
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
