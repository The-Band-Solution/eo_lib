from typing import List
from eo_lib.domain.entities import Project, Team
from eo_lib.domain.repositories import ProjectRepositoryInterface
from libbase.infrastructure.sql_repository import GenericSqlRepository

from eo_lib.infrastructure.database.postgres_client import PostgresClient


class PostgresProjectRepository(
    GenericSqlRepository[Project], ProjectRepositoryInterface
):
    """
    PostgreSQL implementation of the Project Repository.
    """

    def __init__(self):
        """Initializes the repository by getting a session from PostgresClient."""
        client = PostgresClient()
        super().__init__(client.get_session(), Project)

    def add_team_to_project(self, project_id: int, team_id: int) -> None:
        """Assigns a Team to a Project in the database."""
        proj = self._session.query(Project).get(project_id)
        team = self._session.query(Team).get(team_id)
        if proj and team:
            proj.teams.append(team)
            self._session.commit()

    def get_teams(self, project_id: int) -> List[Team]:
        """Retrieves all Teams assigned to a specific Project."""
        proj = self._session.query(Project).get(project_id)
        if proj:
            return proj.teams
        return []
