from typing import List
from eo_lib.domain.repositories.team_repository import TeamRepositoryInterface
from eo_lib.domain.entities.team import Team, TeamMember

class TeamService:
    """
    Business logic for Team management.
    """
    def __init__(self, repo: TeamRepositoryInterface): 
        """Initialize with Repo."""
        self.repo = repo
    
    def create(self, name: str, description: str) -> Team: 
        """Create new team."""
        return self.repo.add(Team(name=name, description=description))
    
    def get(self, id: int) -> Team:
        """Get team by ID."""
        t = self.repo.get(id)
        if not t: raise ValueError(f"Team {id} not found")
        return t

    def update(self, id: int, name: str = None, description: str = None) -> Team:
        t = self.get(id)
        if name: t.name = name
        if description: t.description = description
        return self.repo.update(t)

    def delete(self, id: int) -> None:
        if not self.repo.delete(id): raise ValueError(f"Team {id} not found")

    def list(self) -> List[Team]:
        return self.repo.list()
    
    def add_member(self, team_id: int, person_id: int, role: str, start_date=None, end_date=None) -> TeamMember:
        return self.repo.add_member(TeamMember(
            person_id=person_id, 
            team_id=team_id, 
            role=role,
            start_date=start_date,
            end_date=end_date
        ))

    def remove_member(self, member_id: int) -> None:
        if not self.repo.remove_member(member_id): raise ValueError(f"Member {member_id} not found")

    def get_members(self, team_id: int) -> List[TeamMember]:
        return self.repo.get_members(team_id)
