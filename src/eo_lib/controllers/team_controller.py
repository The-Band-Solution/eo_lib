from typing import List
from datetime import date as date_type
from eo_lib.factories import ServiceFactory
from eo_lib.domain.entities.team import Team, TeamMember

class TeamController:
    """
    Facade for Team operations.
    """
    def __init__(self): 
        """Initialize Service."""
        self.service = ServiceFactory.create_team_service()
    
    def create_team(self, name: str, description: str) -> Team: 
        """Create team."""
        return self.service.create(name, description)
    def get_team(self, id: int) -> Team: return self.service.get(id)
    def update_team(self, id: int, name: str = None, description: str = None) -> Team: return self.service.update(id, name, description)
    def delete_team(self, id: int) -> None: self.service.delete(id)
    def list_teams(self) -> List[Team]: return self.service.list()

    def add_member(self, team_id: int, person_id: int, role: str, start_date: date_type = None, end_date: date_type = None) -> TeamMember: 
        return self.service.add_member(team_id, person_id, role, start_date, end_date)
    def remove_member(self, member_id: int) -> None: self.service.remove_member(member_id)
    def get_members(self, team_id: int) -> List[TeamMember]: return self.service.get_members(team_id)
