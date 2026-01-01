import json
import os
from typing import List, Optional
from eo_lib.domain.repositories import (
    PersonRepositoryInterface,
    TeamRepositoryInterface,
    InitiativeRepository,
    InitiativeTypeRepository,
    OrganizationRepositoryInterface,
    OrganizationalUnitRepositoryInterface,
)
from eo_lib.domain.entities import (
    Person,
    Team,
    TeamMember,
    Initiative,
    InitiativeType,
    Organization,
    OrganizationalUnit,
)

from libbase.infrastructure.json_repository import GenericJsonRepository


class JsonPersonRepository(GenericJsonRepository[Person], PersonRepositoryInterface):
    """JSON implementation of the Person Repository."""

    def __init__(self):
        super().__init__("persons.json", Person)

    def _to_obj(self, data: dict) -> Person:
        """Converts JSON dict to Person entity."""
        return Person(
            name=data["name"],
            emails=data.get("emails", []),
            id=data["id"],
            identification_id=data.get("identification_id"),
        )

    def _to_dict(self, person: Person) -> dict:
        """Converts Person entity to JSON dict."""
        return {
            "id": person.id,
            "name": person.name,
            "emails": (
                [e.email for e in person.emails]
                if hasattr(person, "emails") and person.emails
                else []
            ),
            "identification_id": person.identification_id,
        }


class JsonTeamRepository(GenericJsonRepository[Team], TeamRepositoryInterface):
    """JSON implementation of the Team Repository."""

    def __init__(self):
        super().__init__("teams.json", Team)

    def _to_obj(self, data: dict) -> Team:
        """Converts JSON dict to Team entity."""
        return Team(
            name=data["name"],
            description=data.get("description"),
            id=data["id"],
            short_name=data.get("short_name"),
        )

    def _to_dict(self, team: Team) -> dict:
        """Converts Team entity to JSON dict."""
        return {
            "id": team.id,
            "name": team.name,
            "description": team.description,
            "short_name": team.short_name,
        }

    def add_member(self, member: TeamMember) -> TeamMember:
        """Stub for adding a member in JSON mode."""
        return member

    def remove_member(self, member_id: int) -> bool:
        """Stub for removing a member in JSON mode."""
        return False

    def get_members(self, team_id: int) -> List[TeamMember]:
        """Stub for listing members in JSON mode."""
        return []


class JsonInitiativeRepository(GenericJsonRepository[Initiative], InitiativeRepository):
    """JSON implementation of the Initiative Repository."""

    def __init__(self):
        super().__init__("initiatives.json", Initiative)

    def _to_obj(self, data: dict) -> Initiative:
        return Initiative(
            name=data["name"],
            status=data.get("status", "active"),
            id=data["id"],
            description=data.get("description"),
            initiative_type_id=data.get("initiative_type_id"),
        )

    def _to_dict(self, initiative: Initiative) -> dict:
        return {
            "id": initiative.id,
            "name": initiative.name,
            "status": initiative.status,
            "description": initiative.description,
            "initiative_type_id": initiative.initiative_type_id,
        }


class JsonInitiativeTypeRepository(
    GenericJsonRepository[InitiativeType], InitiativeTypeRepository
):
    """JSON implementation of the InitiativeType Repository."""

    def __init__(self):
        super().__init__("initiative_types.json", InitiativeType)

    def _to_obj(self, data: dict) -> InitiativeType:
        return InitiativeType(
            name=data["name"], description=data.get("description"), id=data["id"]
        )

    def _to_dict(self, obj: InitiativeType) -> dict:
        return {"id": obj.id, "name": obj.name, "description": obj.description}

    def get_by_name(self, name: str) -> Optional[InitiativeType]:
        # Inefficient implementation for JSON (O(N))
        all_types = self.list()
        return next((t for t in all_types if t.name == name), None)


class JsonOrganizationRepository(
    GenericJsonRepository[Organization], OrganizationRepositoryInterface
):
    """JSON implementation of the Organization Repository."""

    def __init__(self):
        super().__init__("organizations.json", Organization)

    def _to_obj(self, data: dict) -> Organization:
        return Organization(
            name=data["name"],
            description=data.get("description"),
            short_name=data.get("short_name"),
            id=data["id"],
        )

    def _to_dict(self, obj: Organization) -> dict:
        return {
            "id": obj.id,
            "name": obj.name,
            "description": obj.description,
            "short_name": obj.short_name,
        }


class JsonOrgUnitRepository(
    GenericJsonRepository[OrganizationalUnit], OrganizationalUnitRepositoryInterface
):
    """JSON implementation of the Organizational Unit Repository."""

    def __init__(self):
        super().__init__("organizational_units.json", OrganizationalUnit)

    def _to_obj(self, data: dict) -> OrganizationalUnit:
        return OrganizationalUnit(
            name=data["name"],
            organization_id=data["organization_id"],
            description=data.get("description"),
            short_name=data.get("short_name"),
            parent_id=data.get("parent_id"),
            id=data["id"],
        )

    def _to_dict(self, obj: OrganizationalUnit) -> dict:
        return {
            "id": obj.id,
            "name": obj.name,
            "organization_id": obj.organization_id,
            "description": obj.description,
            "short_name": obj.short_name,
            "parent_id": obj.parent_id,
        }
