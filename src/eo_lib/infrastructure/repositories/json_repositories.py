import json
import os
import time
from typing import List, Optional, TypeVar, Generic
from abc import abstractmethod
from eo_lib.config import Config
from eo_lib.domain.repositories import (
    GenericRepositoryInterface,
    PersonRepositoryInterface,
    TeamRepositoryInterface,
    ProjectRepositoryInterface,
)
from eo_lib.domain.entities import Person, Team, TeamMember, Project

T = TypeVar('T')

class GenericJsonRepository(GenericRepositoryInterface[T]):
    """
    Generic JSON File Repository implementation.
    
    Provides persistent storage using local JSON files. Each repository manages
    a single file where entities are stored as a JSON array of objects.
    """
    def __init__(self, filename: str):
        """
        Initializes the JSON repository.
        
        Args:
            filename (str): The name of the file (e.g., 'persons.json') to use for storage.
        """
        self.data_dir = Config.get_json_dir()
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.file_path = os.path.join(self.data_dir, filename)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    @abstractmethod
    def _to_obj(self, data: dict) -> T:
        """Converts a raw dictionary from JSON to an entity object."""
        pass

    @abstractmethod
    def _to_dict(self, entity: T) -> dict:
        """Converts an entity object to a serializable dictionary."""
        pass

    def _read_all(self) -> List[dict]:
        """Reads all records from the JSON file."""
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _write_all(self, data: List[dict]):
        """Writes a list of records back to the JSON file."""
        with open(self.file_path, 'w') as f:
            json.dump(data, f, default=str)

    def add(self, entity: T) -> T:
        """
        Appends a new entity to the JSON file.
        
        Args:
            entity (T): The entity to store.
            
        Returns:
            T: The entity with an assigned ID.
        """
        data = self._read_all()
        # Simple ID gen
        entity.id = int(time.time() * 1000) 
        data.append(self._to_dict(entity))
        self._write_all(data)
        return entity

    def get(self, id: int) -> Optional[T]:
        """
        Retrieves an entity by ID from the JSON file.
        
        Args:
            id (int): The unique ID.
            
        Returns:
            Optional[T]: The entity instance or None.
        """
        data = self._read_all()
        for item in data:
            if item.get('id') == id:
                return self._to_obj(item)
        return None

    def update(self, entity: T) -> T:
        """
        Updates an existing record in the JSON file.
        
        Args:
            entity (T): The entity instance with new values.
            
        Returns:
            T: The updated entity.
            
        Raises:
            ValueError: If the entity is not found in the file.
        """
        data = self._read_all()
        updated_data = []
        found = False
        for item in data:
            if item.get('id') == entity.id:
                updated_data.append(self._to_dict(entity))
                found = True
            else:
                updated_data.append(item)
        if not found: raise ValueError("Not found")
        self._write_all(updated_data)
        return entity

    def delete(self, id: int) -> bool:
        """
        Removes a record from the JSON file.
        
        Args:
            id (int): The ID of the record to delete.
            
        Returns:
            bool: True if deleted, False otherwise.
        """
        data = self._read_all()
        new_data = [d for d in data if d.get('id') != id]
        if len(new_data) < len(data):
            self._write_all(new_data)
            return True
        return False

    def list(self) -> List[T]:
        """
        Lists all entities stored in the JSON file.
        
        Returns:
            List[T]: A list of all entities.
        """
        data = self._read_all()
        return [self._to_obj(d) for d in data]


class JsonPersonRepository(GenericJsonRepository[Person], PersonRepositoryInterface):
    """JSON implementation of the Person Repository."""
    def __init__(self):
        super().__init__("persons.json")

    def _to_obj(self, data: dict) -> Person:
        """Converts JSON dict to Person entity."""
        return Person(name=data['name'], emails=data.get('emails', []), id=data['id'], identification_id=data.get('identification_id'))

    def _to_dict(self, person: Person) -> dict:
        """Converts Person entity to JSON dict."""
        return {
            "id": person.id, 
            "name": person.name, 
            "emails": [e.email for e in person.emails] if hasattr(person, 'emails') and person.emails else [],
            "identification_id": person.identification_id
        }

class JsonTeamRepository(GenericJsonRepository[Team], TeamRepositoryInterface):
    """JSON implementation of the Team Repository."""
    def __init__(self):
        super().__init__("teams.json")

    def _to_obj(self, data: dict) -> Team:
        """Converts JSON dict to Team entity."""
        return Team(name=data['name'], description=data.get('description'), id=data['id'], short_name=data.get('short_name'))

    def _to_dict(self, team: Team) -> dict:
        """Converts Team entity to JSON dict."""
        return {"id": team.id, "name": team.name, "description": team.description, "short_name": team.short_name}

    def add_member(self, member: TeamMember) -> TeamMember:
        """Stub for adding a member in JSON mode."""
        pass

    def remove_member(self, member_id: int) -> bool:
        """Stub for removing a member in JSON mode."""
        pass

    def get_members(self, team_id: int) -> List[TeamMember]:
        """Stub for listing members in JSON mode."""
        return []

class JsonProjectRepository(GenericJsonRepository[Project], ProjectRepositoryInterface):
    """JSON implementation of the Project Repository."""
    def __init__(self):
        super().__init__("projects.json")

    def _to_obj(self, data: dict) -> Project:
        """Converts JSON dict to Project entity."""
        return Project(name=data['name'], status=data.get('status', 'active'), id=data['id'], description=data.get('description'))

    def _to_dict(self, project: Project) -> dict:
        """Converts Project entity to JSON dict."""
        return {"id": project.id, "name": project.name, "status": project.status, "description": project.description}

    def add_team_to_project(self, project_id: int, team_id: int) -> None:
        """Stub for assigning a team in JSON mode."""
        pass

    def get_teams(self, project_id: int) -> List[Team]:
        """Stub for listing teams in JSON mode."""
        return []
