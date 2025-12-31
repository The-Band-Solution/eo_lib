from typing import List
from eo_lib.domain.entities import Team, TeamMember
from eo_lib.domain.repositories import TeamRepositoryInterface
from libbase.infrastructure.sql_repository import GenericSqlRepository

from eo_lib.infrastructure.database.postgres_client import PostgresClient


class PostgresTeamRepository(GenericSqlRepository[Team], TeamRepositoryInterface):
    """
    PostgreSQL implementation of the Team Repository.
    """

    def __init__(self):
        """Initializes the repository by getting a session from PostgresClient."""
        client = PostgresClient()
        super().__init__(client.get_session(), Team)

    def add_member(self, member: TeamMember) -> TeamMember:
        """Persists a new TeamMember association in the database."""
        try:
            self._session.add(member)
            self._session.commit()
            self._session.refresh(member)
            return member
        except Exception:
            self._session.rollback()
            raise

    def remove_member(self, member_id: int) -> bool:
        """Deletes a TeamMember association for the database."""
        db_obj = self._session.query(TeamMember).filter_by(id=member_id).first()
        if db_obj:
            self._session.delete(db_obj)
            self._session.commit()
            return True
        return False

    def get_members(self, team_id: int) -> List[TeamMember]:
        """Retrieves all membership associations for a specific Team."""
        return self._session.query(TeamMember).filter_by(team_id=team_id).all()
