from typing import List
from eo_lib.domain.entities.project import Project
from eo_lib.domain.entities.team import Team
from eo_lib.domain.repositories.project_repository import ProjectRepositoryInterface
from eo_lib.infrastructure.repositories.generic_postgres_repository import GenericPostgresRepository

class PostgresProjectRepository(GenericPostgresRepository[Project], ProjectRepositoryInterface):
    """
    Repository for Project entity (Unified Model).
    """
    def __init__(self):
        super().__init__(Project)

    def add_team_to_project(self, project_id: int, team_id: int) -> None:
        session = self.client.get_session()
        try:
            proj = session.query(Project).get(project_id)
            team = session.query(Team).get(team_id)
            if proj and team:
                proj.teams.append(team)
                session.commit()
        finally: session.close()

    def get_teams(self, project_id: int) -> List[Team]:
         session = self.client.get_session()
         try:
             proj = session.query(Project).get(project_id)
             if proj:
                 return proj.teams
             return []
         finally: session.close()
