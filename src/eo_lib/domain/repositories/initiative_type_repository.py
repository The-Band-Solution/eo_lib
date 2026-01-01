from abc import ABC, abstractmethod
from typing import List, Optional
from eo_lib.domain.entities.initiative import InitiativeType


class InitiativeTypeRepository(ABC):
    @abstractmethod
    def add(self, initiative_type: InitiativeType) -> InitiativeType:
        pass

    @abstractmethod
    def get(self, id: int) -> Optional[InitiativeType]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[InitiativeType]:
        pass

    @abstractmethod
    def list(self) -> List[InitiativeType]:
        pass

    @abstractmethod
    def update(self, initiative_type: InitiativeType) -> InitiativeType:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
