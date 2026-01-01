from typing import List, Optional
from eo_lib.domain.entities import Organization
from eo_lib.domain.repositories import OrganizationRepositoryInterface
from libbase.services.generic_service import GenericService


class OrganizationService(GenericService[Organization]):
    """
    Service for Organization-related business logic.
    """

    def __init__(self, repository: OrganizationRepositoryInterface):
        super().__init__(repository)

    def create_organization(
        self, name: str, description: str = None, short_name: str = None
    ) -> Organization:
        """
        Creates a new Organization.
        """
        org = Organization(name=name, description=description, short_name=short_name)
        self.create(org)
        return org

    def update_organization_details(
        self, id: int, name: str = None, description: str = None, short_name: str = None
    ) -> Organization:
        """
        Updates organization metadata.
        """
        org = self.get_by_id(id)
        if not org:
            raise ValueError(f"Organization {id} not found")

        if name:
            org.name = name
        if description:
            org.description = description
        if short_name:
            org.short_name = short_name

        self.update(org)
        return org
