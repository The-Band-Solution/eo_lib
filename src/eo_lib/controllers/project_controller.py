from typing import List
from eo_lib.factories import ServiceFactory
from eo_lib.domain.entities.project import Project
from eo_lib.domain.entities.team import Team

class ProjectController:
    """
    Facade for Project operations.
    """
    def __init__(self):
        """Initialize Service."""
        self.service = ServiceFactory.create_project_service()

    def create_project(self, name: str, description: str = None, start_date = None, end_date = None) -> Project: 
        """Create project."""
        return self.service.create(name, description, start_date, end_date)
    def get_project(self, id: int) -> Project: return self.service.get(id)
    def update_project(self, id: int, name: str = None, status: str = None, description: str = None, start_date = None, end_date = None) -> Project: return self.service.update(id, name, status, description, start_date, end_date)
    def delete_project(self, id: int) -> None: self.service.delete(id)
    def list_projects(self) -> List[Project]: return self.service.list()

    def assign_team(self, project_id: int, team_id: int): self.service.assign_team(project_id, team_id)
    def get_teams(self, project_id: int) -> List[Team]: return self.service.get_teams(project_id)
