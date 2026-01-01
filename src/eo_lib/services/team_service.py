from typing import List
from eo_lib.domain.repositories import TeamRepositoryInterface
from eo_lib.domain.entities import Team, TeamMember
from libbase.services.generic_service import GenericService


class TeamService(GenericService[Team]):
    """
    Service for managing Team-related business logic.
    Inherits generic CRUD from GenericService.
    """

    def __init__(self, repo: TeamRepositoryInterface):
        super().__init__(repo)
        self.repo = repo

    def create_team(self, name: str, description: str) -> Team:
        """
        Creates and stores a new Team using arguments.
        """
        team = Team(name=name, description=description)
        self.create(team)
        return team

    def update_team_details(self, id: int, name: str = None, description: str = None) -> Team:
        """
        Updates an existing Team's information.
        """
        t = self.get_by_id(id)
        if not t:
            raise ValueError(f"Team {id} not found")
            
        if name:
            t.name = name
        if description:
            t.description = description
            
        self.update(t)
        return t

    def add_member(
        self,
        team_id: int,
        person_id: int,
        role: object = None,
        role_id: int = None,
        start_date=None,
        end_date=None,
    ) -> TeamMember:
        """
        Adds a Person to a Team.
        """
        return self.repo.add_member(
            TeamMember(
                person_id=person_id,
                team_id=team_id,
                role=role,
                role_id=role_id,
                start_date=start_date,
                end_date=end_date,
            )
        )

    def remove_member(self, member_id: int) -> None:
        """
        Removes a membership association by ID.
        """
        if not self.repo.remove_member(member_id):
            raise ValueError(f"Member {member_id} not found")

    def get_members(self, team_id: int) -> List[TeamMember]:
        """
        Retrieves all members of a specific Team.
        """
        return self.repo.get_members(team_id)
