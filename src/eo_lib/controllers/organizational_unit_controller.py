from eo_lib.factories import ServiceFactory
from eo_lib.domain.entities import OrganizationalUnit
from libbase.controllers.generic_controller import GenericController


class OrganizationalUnitController(GenericController[OrganizationalUnit]):
    """
    Controller for Organizational Unit-related operations.
    Acts as a facade for the OrganizationalUnitService.
    """

    def __init__(self):
        service = ServiceFactory.create_organizational_unit_service()
        super().__init__(service)

    def create_unit(
        self,
        name: str,
        organization_id: int,
        description: str = None,
        short_name: str = None,
        parent_id: int = None,
    ) -> OrganizationalUnit:
        """
        Creates a new organizational unit.
        """
        return self._service.create_unit(
            name, organization_id, description, short_name, parent_id
        )

    def update_unit(
        self,
        id: int,
        name: str = None,
        description: str = None,
        short_name: str = None,
        parent_id: int = None,
    ) -> OrganizationalUnit:
        """
        Updates unit metadata.
        """
        return self._service.update_unit_details(
            id, name, description, short_name, parent_id
        )
