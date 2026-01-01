from typing import List
from datetime import date as date_type
from eo_lib.factories import ServiceFactory
from eo_lib.domain.entities.team import Team, TeamMember
from libbase.controllers.generic_controller import GenericController


class TeamController(GenericController[Team]):
    """
    Controller for Team-related operations.
    Acts as a facade for the TeamService.
    """

    def __init__(self):
        service = ServiceFactory.create_team_service()
        super().__init__(service)

    def create_team(self, name: str, description: str) -> Team:
        """
        Creates a new team.
        Wraps service.create_team.
        """
        return self._service.create_team(name, description)

    def update_team(self, id: int, name: str = None, description: str = None) -> Team:
        """Updates team metadata."""
        return self._service.update_team_details(id, name, description)
    
    # GenericController provides get_by_id, get_all, delete via inheritance (mapped to _service)
    # But for backward compatibility with demo.py (until updated), we might keep aliases if needed.
    # The GenericController has get_by_id, get_all.
    # The Plan says "demo.py will be updated".
    # So I REMOVE get_team, list_teams, delete_team in favor of inherited methods.

    def add_member(
        self,
        team_id: int,
        person_id: int,
        role: str,
        start_date: date_type = None,
        end_date: date_type = None,
    ) -> TeamMember:
        """
        Enrolls a person into a team with a specific role.
        """
        return self._service.add_member(
            team_id, person_id, role=role, start_date=start_date, end_date=end_date
        )

    def remove_member(self, member_id: int) -> None:
        """Removes a person's membership from a team."""
        self._service.remove_member(member_id)

    def get_members(self, team_id: int) -> List[TeamMember]:
        """Lists all members enrolled in a specific team."""
        return self._service.get_members(team_id)
