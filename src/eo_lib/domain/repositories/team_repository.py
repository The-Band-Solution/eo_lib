from abc import abstractmethod
from typing import List
from eo_lib.domain.entities import Team, TeamMember
from libbase.infrastructure.interface import IRepository as GenericRepositoryInterface


class TeamRepositoryInterface(GenericRepositoryInterface[Team]):
    """
    Interface for Team Repository.

    Extends GenericRepositoryInterface to provide specific data access
    operations for Team entities, including member enrollment and management.
    """

    @abstractmethod
    def add_member(self, member: TeamMember) -> TeamMember:
        """
        Enrolls a Person into a Team by creating a TeamMember association.

        Args:
            member (TeamMember): The association object between Person and Team.

        Returns:
            TeamMember: The stored association instance.
        """
        pass

    @abstractmethod
    def remove_member(self, member_id: int) -> bool:
        """
        Removes a Person from a Team membership.

        Args:
            member_id (int): ID of the TeamMember association to remove.

        Returns:
            bool: True if removed successfully, False otherwise.
        """
        pass

    @abstractmethod
    def get_members(self, team_id: int) -> List[TeamMember]:
        """
        Retrieves all members of a specific Team.

        Args:
            team_id (int): ID of the Team.

        Returns:
            List[TeamMember]: A list of TeamMember association entities.
        """
        pass
