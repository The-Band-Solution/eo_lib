from datetime import datetime
from typing import List, Optional, Dict, Any
from eo_lib.services.initiative_service import InitiativeService
from eo_lib.domain.entities.initiative import Initiative, InitiativeType
from eo_lib.factories import ServiceFactory


class InitiativeController:
    """
    Controller for Initiative-related operations.
    Acts as a Facade to the InitiativeService.
    """

    def __init__(self):
        self.service = ServiceFactory.create_initiative_service()

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

        Args:
            name (str): The name of the initiative.
            description (str, optional): Meaningful description.
            start_date (datetime, optional): Start date.
            end_date (datetime, optional): End date.
            initiative_type_name (str, optional): Name of the initiative type.

        Returns:
            dict: The created initiative details.
        """
        initiative = self.service.create_initiative(
            name, description, start_date, end_date, initiative_type_name
        )
        return self._to_dto(initiative)

    def create_initiative_type(
        self, name: str, description: str = None
    ) -> Dict[str, Any]:
        """
        Creates a new initiative type.

        Args:
            name (str): The name of the type.
            description (str, optional): Description of the type.

        Returns:
            dict: The created type details.
        """
        itype = self.service.create_initiative_type(name, description)
        return {"id": itype.id, "name": itype.name, "description": itype.description}

    def list_initiatives(self) -> List[Dict[str, Any]]:
        """
        Lists all initiatives.

        Returns:
            List[dict]: List of initiative DTOs.
        """
        initiatives = self.service.list_initiatives()
        return [self._to_dto(p) for p in initiatives]

    def list_initiative_types(self) -> List[Dict[str, Any]]:
        """
        Lists all initiative types.

        Returns:
            List[dict]: List of type DTOs.
        """
        types = self.service.list_initiative_types()
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
        initiative = self.service.update_initiative(
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

        Args:
            initiative_id (int): Encoded Initiative ID.
            team_id (int): Encoded Team ID.
        """
        self.service.assign_team(initiative_id, team_id)

    def get_teams(self, initiative_id: int) -> List[Dict[str, Any]]:
        """
        Lists teams assigned to an initiative.

        Args:
            initiative_id (int): Initiative ID.
        Returns:
            List[dict]: List of Team DTOs.
        """
        teams = self.service.get_teams(initiative_id)
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
