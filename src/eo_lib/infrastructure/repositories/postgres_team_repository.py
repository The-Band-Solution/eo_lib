from typing import List
from eo_lib.domain.entities import Team, TeamMember
from eo_lib.domain.repositories import TeamRepositoryInterface
from eo_lib.infrastructure.repositories.generic_postgres_repository import GenericPostgresRepository

class PostgresTeamRepository(GenericPostgresRepository[Team], TeamRepositoryInterface):
    """
    PostgreSQL implementation of the Team Repository.
    
    Inherits generic CRUD from GenericPostgresRepository and implements
    Team-specific operations like member management.
    """
    def __init__(self):
        """Initializes the repository with the Team model."""
        super().__init__(Team)

    def add_member(self, member: TeamMember) -> TeamMember:
        """
        Persists a new TeamMember association in the database.
        
        Args:
            member (TeamMember): The association entity to store.
            
        Returns:
            TeamMember: The persisted association.
        """
        session = self.client.get_session()
        try:
            session.add(member)
            session.commit()
            session.refresh(member)
            return member
        finally: session.close()

    def remove_member(self, member_id: int) -> bool:
        """
        Deletes a TeamMember association for the database.
        
        Args:
            member_id (int): ID of the membership to remove.
            
        Returns:
            bool: True if deleted, False otherwise.
        """
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
        """
        Retrieves all membership associations for a specific Team.
        
        Args:
            team_id (int): ID of the Team.
            
        Returns:
            List[TeamMember]: List of membership entities.
        """
        session = self.client.get_session()
        try:
            return session.query(TeamMember).filter_by(team_id=team_id).all()
        finally: session.close()
