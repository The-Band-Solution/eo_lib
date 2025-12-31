from abc import abstractmethod
from typing import List
from eo_lib.domain.entities import Project
from eo_lib.domain.entities import Team
from .generic_repository import GenericRepositoryInterface

class ProjectRepositoryInterface(GenericRepositoryInterface[Project]):
    """
    Interface for Project Repository.
    
    Extends GenericRepositoryInterface to provide specific data access
    operations for Project entities, including team management within projects.
    """

    @abstractmethod
    def add_team_to_project(self, project_id: int, team_id: int) -> None:
        """
        Assigns a Team to a Project.
        
        Args:
            project_id (int): ID of the target Project.
            team_id (int): ID of the Team to assign.
        """
        pass

    @abstractmethod
    def get_teams(self, project_id: int) -> List[Team]:
        """
        Retrieves all Teams currently assigned to a specific Project.
        
        Args:
            project_id (int): ID of the Project.
            
        Returns:
            List[Team]: A list of assigned Team entities.
        """
        pass
