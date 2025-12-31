from abc import abstractmethod
from typing import List
from eo_lib.domain.entities.team import Team, TeamMember
from eo_lib.domain.repositories.generic_repository import GenericRepositoryInterface

class TeamRepositoryInterface(GenericRepositoryInterface[Team]):
    """
    Interface for Team Repository.
    Inherits standard CRUD from GenericRepositoryInterface.
    Adds Member management.
    """
    
    @abstractmethod
    def add_member(self, member: TeamMember) -> TeamMember: pass
    @abstractmethod
    def remove_member(self, member_id: int) -> bool: pass
    @abstractmethod
    def get_members(self, team_id: int) -> List[TeamMember]: pass
