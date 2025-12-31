from typing import List
from eo_lib.domain.repositories import TeamRepositoryInterface
from eo_lib.domain.entities import Team, TeamMember


class TeamService:
    """
    Service for managing Team-related business logic.

    Provides high-level operations for creating, retrieving, updating,
    and deleting Teams, as well as managing team memberships and roles.
    """

    def __init__(self, repo: TeamRepositoryInterface):
        """
        Initializes the TeamService with a specific repository.

        Args:
            repo (TeamRepositoryInterface): The repository implementation for data access.
        """
        self.repo = repo

    def create(self, name: str, description: str) -> Team:
        """
        Creates and stores a new Team.

        Args:
            name (str): The name of the team.
            description (str): A brief summary of the team's purpose.

        Returns:
            Team: The newly created and stored Team entity.
        """
        team = Team(name=name, description=description)
        self.repo.add(team)
        return team

    def get(self, id: int) -> Team:
        """
        Retrieves a Team by its unique identifier.

        Args:
            id (int): The ID of the Team to retrieve.

        Returns:
            Team: The retrieved Team entity.

        Raises:
            ValueError: If no Team is found with the given ID.
        """
        t = self.repo.get_by_id(id)
        if not t:
            raise ValueError(f"Team {id} not found")
        return t

    def update(self, id: int, name: str = None, description: str = None) -> Team:
        """
        Updates an existing Team's information.

        Args:
            id (int): ID of the Team to update.
            name (str, optional): New name. Defaults to None.
            description (str, optional): New description. Defaults to None.

        Returns:
            Team: The updated Team entity.

        Raises:
            ValueError: If no Team is found with the given ID.
        """
        t = self.get(id)
        if name:
            t.name = name
        if description:
            t.description = description
        self.repo.update(t)
        return t

    def delete(self, id: int) -> None:
        """
        Deletes a Team from the system.

        Args:
            id (int): ID of the Team to delete.

        Raises:
            ValueError: If no Team is found with the given ID.
        """
        self.repo.delete(id)

    def list(self) -> List[Team]:
        """
        Retrieves a list of all Teams in the system.

        Returns:
            List[Team]: A list containing all Team entities.
        """
        return self.repo.get_all()

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

        Args:
            team_id (int): The ID of the Team.
            person_id (int): The ID of the Person to add.
            role (Role, optional): A Role object to assign. Defaults to None.
            role_id (int, optional): The ID of a Role to assign. Defaults to None.
            start_date (date, optional): Participation start date. Defaults to None.
            end_date (date, optional): Participation end date. Defaults to None.

        Returns:
            TeamMember: The created membership association.
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

        Args:
            member_id (int): The ID of the TeamMember association.

        Raises:
            ValueError: If the membership is not found.
        """
        if not self.repo.remove_member(member_id):
            raise ValueError(f"Member {member_id} not found")

    def get_members(self, team_id: int) -> List[TeamMember]:
        """
        Retrieves all members of a specific Team.

        Args:
            team_id (int): The ID of the Team.

        Returns:
            List[TeamMember]: A list of TeamMember association entities.
        """
        return self.repo.get_members(team_id)
