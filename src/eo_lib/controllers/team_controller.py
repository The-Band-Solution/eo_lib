from typing import List
from datetime import date as date_type
from eo_lib.factories import ServiceFactory
from eo_lib.domain.entities.team import Team, TeamMember


class TeamController:
    """
    Controller for Team-related operations.

    Acts as a facade for the TeamService, coordinating group management
    and person enrollment into specific teams.
    """

    def __init__(self):
        """Initializes the Controller by creating the required TeamService."""
        self.service = ServiceFactory.create_team_service()

    def create_team(self, name: str, description: str) -> Team:
        """
        Creates a new team.

        Args:
            name (str): Unique team name.
            description (str): Functional purpose of the team.

        Returns:
            Team: The newly created Team entity.
        """
        return self.service.create(name, description)

    def get_team(self, id: int) -> Team:
        """Retrieves a team by its unique ID."""
        return self.service.get(id)

    def update_team(self, id: int, name: str = None, description: str = None) -> Team:
        """Updates team metadata."""
        return self.service.update(id, name, description)

    def delete_team(self, id: int) -> None:
        """Removes a team from the system."""
        self.service.delete(id)

    def list_teams(self) -> List[Team]:
        """Retrieves a list of all existing teams."""
        return self.service.list()

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

        Args:
            team_id (int): Target team.
            person_id (int): Person to enroll.
            role (str): Role description.
            start_date (date, optional): Enrollment start.
            end_date (date, optional): Enrollment end.

        Returns:
            TeamMember: The newly created membership record.
        """
        return self.service.add_member(
            team_id, person_id, role=role, start_date=start_date, end_date=end_date
        )

    def remove_member(self, member_id: int) -> None:
        """Removes a person's membership from a team."""
        self.service.remove_member(member_id)

    def get_members(self, team_id: int) -> List[TeamMember]:
        """Lists all members enrolled in a specific team."""
        return self.service.get_members(team_id)
