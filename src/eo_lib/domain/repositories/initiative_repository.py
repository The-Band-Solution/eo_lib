from abc import ABC, abstractmethod
from typing import List, Optional
from eo_lib.domain.entities.initiative import Initiative


class InitiativeRepository(ABC):
    @abstractmethod
    def add(self, initiative: Initiative) -> Initiative:
        pass

    @abstractmethod
    def get(self, id: int) -> Optional[Initiative]:
        pass

    @abstractmethod
    def list(self) -> List[Initiative]:
        pass

    @abstractmethod
    def update(self, initiative: Initiative) -> Initiative:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
