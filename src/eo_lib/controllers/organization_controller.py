from eo_lib.factories import ServiceFactory
from eo_lib.domain.entities import Organization
from libbase.controllers.generic_controller import GenericController


class OrganizationController(GenericController[Organization]):
    """
    Controller for Organization-related operations.
    Acts as a facade for the OrganizationService.
    """

    def __init__(self):
        service = ServiceFactory.create_organization_service()
        super().__init__(service)

    def create_organization(
        self, name: str, description: str = None, short_name: str = None
    ) -> Organization:
        """
        Creates a new organization.
        """
        return self._service.create_organization(name, description, short_name)

    def update_organization(
        self, id: int, name: str = None, description: str = None, short_name: str = None
    ) -> Organization:
        """
        Updates organization metadata.
        """
        return self._service.update_organization_details(id, name, description, short_name)
