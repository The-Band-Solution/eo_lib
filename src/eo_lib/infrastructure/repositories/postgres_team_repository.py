from typing import List
from eo_lib.domain.entities.team import Team, TeamMember
from eo_lib.domain.repositories.team_repository import TeamRepositoryInterface
from eo_lib.infrastructure.repositories.generic_postgres_repository import GenericPostgresRepository

class PostgresTeamRepository(GenericPostgresRepository[Team], TeamRepositoryInterface):
    """
    Repository for Team entity (Unified Model).
    """
    def __init__(self):
        super().__init__(Team)

    def add_member(self, member: TeamMember) -> TeamMember:
        session = self.client.get_session()
        try:
            session.add(member)
            session.commit()
            session.refresh(member)
            return member
        finally: session.close()

    def remove_member(self, member_id: int) -> bool:
        session = self.client.get_session()
        try:
            db_obj = session.query(TeamMember).filter_by(id=member_id).first()
            if db_obj:
                session.delete(db_obj)
                session.commit()
                return True
            return False
        finally: session.close()

    def get_members(self, team_id: int) -> List[TeamMember]:
        session = self.client.get_session()
        try:
            return session.query(TeamMember).filter_by(team_id=team_id).all()
        finally: session.close()
