from typing import List
from eo_lib.factories import ServiceFactory
from eo_lib.domain.entities.project import Project
from eo_lib.domain.entities.team import Team

class ProjectController:
    """
    Controller for Project-related operations.
    
    Acts as a facade for the ProjectService, providing entry points for
    managing Projects and their organizational structure.
    """
    def __init__(self):
        """Initializes the Controller by creating the required ProjectService."""
        self.service = ServiceFactory.create_project_service()

    def create_project(self, name: str, description: str = None, start_date = None, end_date = None) -> Project: 
        """
        Creates a new project record.
        
        Args:
            name (str): The project name.
            description (str, optional): Summary of goals. Defaults to None.
            start_date (datetime, optional): Start date. Defaults to None.
            end_date (datetime, optional): End date. Defaults to None.
            
        Returns:
            Project: The newly created Project entity.
        """
        return self.service.create(name, description, start_date, end_date)

    def get_project(self, id: int) -> Project:
        """Retrieves a project by its ID."""
        return self.service.get(id)

    def update_project(self, id: int, name: str = None, status: str = None, description: str = None, start_date = None, end_date = None) -> Project:
        """Updates an existing project record's settings."""
        return self.service.update(id, name, status, description, start_date, end_date)

    def delete_project(self, id: int) -> None:
        """Deletes a project record from the system."""
        self.service.delete(id)

    def list_projects(self) -> List[Project]:
        """Retrieves a list of all current projects."""
        return self.service.list()

    def assign_team(self, project_id: int, team_id: int):
        """Assigns a target team to work on a specific project."""
        self.service.assign_team(project_id, team_id)

    def get_teams(self, project_id: int) -> List[Team]:
        """Retrieves all teams currently assigned to a project."""
        return self.service.get_teams(project_id)
