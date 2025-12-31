import json
import os
import time
from typing import List, Optional, TypeVar, Generic
from abc import abstractmethod
from eo_lib.config import Config
from eo_lib.domain.repositories.generic_repository import GenericRepositoryInterface
from eo_lib.domain.entities.person import Person
from eo_lib.domain.repositories.person_repository import PersonRepositoryInterface
from eo_lib.domain.entities.team import Team, TeamMember
from eo_lib.domain.repositories.team_repository import TeamRepositoryInterface
from eo_lib.domain.entities.project import Project
from eo_lib.domain.repositories.project_repository import ProjectRepositoryInterface

T = TypeVar('T')

class GenericJsonRepository(GenericRepositoryInterface[T]):
    """
    Generic JSON File Repository.
    """
    def __init__(self, filename: str):
        self.data_dir = Config.get_json_dir()
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.file_path = os.path.join(self.data_dir, filename)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    @abstractmethod
    def _to_obj(self, data: dict) -> T: pass

    @abstractmethod
    def _to_dict(self, entity: T) -> dict: pass

    def _read_all(self) -> List[dict]:
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _write_all(self, data: List[dict]):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, default=str)

    def add(self, entity: T) -> T:
        data = self._read_all()
        # Simple ID gen
        entity.id = int(time.time() * 1000) 
        data.append(self._to_dict(entity))
        self._write_all(data)
        return entity

    def get(self, id: int) -> Optional[T]:
        data = self._read_all()
        for item in data:
            if item.get('id') == id:
                return self._to_obj(item)
        return None

    def update(self, entity: T) -> T:
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
        data = self._read_all()
        new_data = [d for d in data if d.get('id') != id]
        if len(new_data) < len(data):
            self._write_all(new_data)
            return True
        return False

    def list(self) -> List[T]:
        data = self._read_all()
        return [self._to_obj(d) for d in data]


class JsonPersonRepository(GenericJsonRepository[Person], PersonRepositoryInterface):
    def __init__(self):
        super().__init__("persons.json")

    def _to_obj(self, data: dict) -> Person:
        return Person(name=data['name'], email=data['email'], id=data['id'])

    def _to_dict(self, person: Person) -> dict:
        return {"id": person.id, "name": person.name, "email": person.email}

class JsonTeamRepository(GenericJsonRepository[Team], TeamRepositoryInterface):
    def __init__(self):
        super().__init__("teams.json")

    def _to_obj(self, data: dict) -> Team:
        return Team(name=data['name'], description=data.get('description'), id=data['id'])

    def _to_dict(self, team: Team) -> dict:
        return {"id": team.id, "name": team.name, "description": team.description}

    def add_member(self, member: TeamMember) -> TeamMember:
        # Stub implementation for JSON mode
        pass

    def remove_member(self, member_id: int) -> bool:
        pass

    def get_members(self, team_id: int) -> List[TeamMember]:
        return []

class JsonProjectRepository(GenericJsonRepository[Project], ProjectRepositoryInterface):
    def __init__(self):
        super().__init__("projects.json")

    def _to_obj(self, data: dict) -> Project:
        return Project(name=data['name'], status=data.get('status', 'active'), id=data['id'])

    def _to_dict(self, project: Project) -> dict:
        return {"id": project.id, "name": project.name, "status": project.status}

    def add_team_to_project(self, project_id: int, team_id: int) -> None:
        pass

    def get_teams(self, project_id: int) -> List[Team]:
        return []
