from datetime import datetime
from typing import List, Optional, Dict, Any
from eo_lib.domain.entities.initiative import Initiative
from eo_lib.factories import ServiceFactory
from libbase.controllers.generic_controller import GenericController


class InitiativeController(GenericController[Initiative]):
    """
    Controller for Initiative-related operations.
    Acts as a Facade to the InitiativeService.
    """

    def __init__(self):
        service = ServiceFactory.create_initiative_service()
        super().__init__(service)

    def create_initiative(
        self,
        name: str,
        description: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        initiative_type_name: str = None,
    ) -> Dict[str, Any]:
        """
        Creates a new initiative.
        Wraps service.create_initiative_with_details.
        """
        initiative = self._service.create_initiative_with_details(
            name, description, start_date, end_date, initiative_type_name
        )
        return self._to_dto(initiative)

    def create_initiative_type(
        self, name: str, description: str = None
    ) -> Dict[str, Any]:
        """
        Creates a new initiative type.
        """
        itype = self._service.create_initiative_type(name, description)
        return {"id": itype.id, "name": itype.name, "description": itype.description}

    def list_initiatives(self) -> List[Dict[str, Any]]:
        """
        Lists all initiatives.
        """
        # Using generic get_all() from parent
        initiatives = self.get_all() 
        return [self._to_dto(p) for p in initiatives]

    def list_initiative_types(self) -> List[Dict[str, Any]]:
        """
        Lists all initiative types.
        """
        types = self._service.list_initiative_types()
        return [
            {"id": t.id, "name": t.name, "description": t.description} for t in types
        ]

    def update_initiative(
        self,
        initiative_id: int,
        name: str = None,
        description: str = None,
        status: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        initiative_type_name: str = None,
    ) -> Dict[str, Any]:
        """
        Updates an existing initiative.
        """
        initiative = self._service.update_initiative_details(
            initiative_id,
            name,
            description,
            status,
            start_date,
            end_date,
            initiative_type_name,
        )
        return self._to_dto(initiative)

    def assign_team(self, initiative_id: int, team_id: int) -> None:
        """
        Assigns a team to an initiative.
        """
        self._service.assign_team(initiative_id, team_id)

    def get_teams(self, initiative_id: int) -> List[Dict[str, Any]]:
        """
        Lists teams assigned to an initiative.
        """
        teams = self._service.get_teams(initiative_id)
        return [{"id": t.id, "name": t.name} for t in teams]

    def _to_dto(self, initiative: Initiative) -> Dict[str, Any]:
        return {
            "id": initiative.id,
            "name": initiative.name,
            "status": initiative.status,
            "description": initiative.description,
            "start_date": (
                initiative.start_date.isoformat() if initiative.start_date else None
            ),
            "end_date": (
                initiative.end_date.isoformat() if initiative.end_date else None
            ),
            "initiative_type": (
                initiative.initiative_type.name if initiative.initiative_type else None
            ),
        }
