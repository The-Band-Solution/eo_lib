from abc import abstractmethod
from typing import Optional
from eo_lib.domain.entities.initiative import InitiativeType
from libbase.infrastructure.interface import IRepository as GenericRepositoryInterface


class InitiativeTypeRepository(GenericRepositoryInterface[InitiativeType]):
    """
    Interface for InitiativeType Repository.
    """

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[InitiativeType]:
        pass
