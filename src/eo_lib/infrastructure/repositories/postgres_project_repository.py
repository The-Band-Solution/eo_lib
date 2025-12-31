from typing import List
from eo_lib.domain.entities import Project, Team
from eo_lib.domain.repositories import ProjectRepositoryInterface
from eo_lib.infrastructure.repositories.generic_postgres_repository import GenericPostgresRepository

class PostgresProjectRepository(GenericPostgresRepository[Project], ProjectRepositoryInterface):
    """
    PostgreSQL implementation of the Project Repository.
    
    Inherits generic CRUD from GenericPostgresRepository and implements
    Project-specific operations like team assignment.
    """
    def __init__(self):
        """Initializes the repository with the Project model."""
        super().__init__(Project)

    def add_team_to_project(self, project_id: int, team_id: int) -> None:
        """
        Assigns a Team to a Project in the database.
        
        Args:
            project_id (int): ID of the Project.
            team_id (int): ID of the Team to assign.
        """
        session = self.client.get_session()
        try:
            proj = session.query(Project).get(project_id)
            team = session.query(Team).get(team_id)
            if proj and team:
                proj.teams.append(team)
                session.commit()
        finally: session.close()

    def get_teams(self, project_id: int) -> List[Team]:
        """
        Retrieves all Teams assigned to a specific Project.
        
        Args:
            project_id (int): ID of the Project.
            
        Returns:
            List[Team]: List of assigned Teams.
        """
        session = self.client.get_session()
        try:
            proj = session.query(Project).get(project_id)
            if proj:
                return proj.teams
            return []
        finally: session.close()
