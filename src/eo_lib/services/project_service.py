from typing import List
from eo_lib.domain.repositories.project_repository import ProjectRepositoryInterface
from eo_lib.domain.entities.project import Project
from eo_lib.domain.entities.team import Team

class ProjectService:
    """
    Business logic for Project management.
    """
    def __init__(self, repo: ProjectRepositoryInterface): 
        """Initialize with Repo."""
        self.repo = repo
    
    def create(self, name: str, description: str = None, start_date = None, end_date = None) -> Project: 
        """Create new project."""
        return self.repo.add(Project(name=name, description=description, start_date=start_date, end_date=end_date))
    
    def get(self, id: int) -> Project:
        """Get project by ID."""
        p = self.repo.get(id)
        if not p: raise ValueError(f"Project {id} not found")
        return p

    def update(self, id: int, name: str = None, status: str = None, description: str = None, start_date = None, end_date = None) -> Project:
        p = self.get(id)
        if name: p.name = name
        if status: p.status = status
        if description: p.description = description
        if start_date: p.start_date = start_date
        if end_date: p.end_date = end_date
        return self.repo.update(p)

    def delete(self, id: int) -> None:
        if not self.repo.delete(id): raise ValueError(f"Project {id} not found")

    def list(self) -> List[Project]:
        return self.repo.list()

    def assign_team(self, project_id: int, team_id: int): 
        self.repo.add_team_to_project(project_id, team_id)

    def get_teams(self, project_id: int) -> List[Team]:
        return self.repo.get_teams(project_id)
