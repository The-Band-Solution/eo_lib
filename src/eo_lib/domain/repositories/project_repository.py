from abc import abstractmethod
from typing import List
from eo_lib.domain.entities.project import Project
from eo_lib.domain.entities.team import Team
from eo_lib.domain.repositories.generic_repository import GenericRepositoryInterface

class ProjectRepositoryInterface(GenericRepositoryInterface[Project]):
    """
    Interface for Project Repository.
    Inherits standard CRUD from GenericRepositoryInterface.
    Adds Team assignment.
    """

    @abstractmethod
    def add_team_to_project(self, project_id: int, team_id: int) -> None: pass
    @abstractmethod
    def get_teams(self, project_id: int) -> List[Team]: pass
