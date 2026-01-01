from typing import List, Optional
from eo_lib.domain.entities import OrganizationalUnit
from eo_lib.domain.repositories import OrganizationalUnitRepositoryInterface
from libbase.services.generic_service import GenericService


class OrganizationalUnitService(GenericService[OrganizationalUnit]):
    """
    Service for Organizational Unit-related business logic.
    Supports hierarchical structures.
    """

    def __init__(self, repository: OrganizationalUnitRepositoryInterface):
        super().__init__(repository)

    def create_unit(
        self,
        name: str,
        organization_id: int,
        description: str = None,
        short_name: str = None,
        parent_id: int = None,
    ) -> OrganizationalUnit:
        """
        Creates a new Organizational Unit.
        """
        unit = OrganizationalUnit(
            name=name,
            organization_id=organization_id,
            description=description,
            short_name=short_name,
            parent_id=parent_id,
        )
        self.create(unit)
        return unit

    def update_unit_details(
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
        unit = self.get_by_id(id)
        if not unit:
            raise ValueError(f"Organizational Unit {id} not found")

        if name:
            unit.name = name
        if description:
            unit.description = description
        if short_name:
            unit.short_name = short_name
        if parent_id is not None:
            unit.parent_id = parent_id

        self.update(unit)
        return unit
