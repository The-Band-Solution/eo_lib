import json
import os
import time
from typing import List, Optional, TypeVar, Generic
from abc import abstractmethod
from eo_lib.config import Config
from eo_lib.domain.repositories import (
    GenericRepositoryInterface,
    PersonRepositoryInterface,
    TeamRepositoryInterface,
    ProjectRepositoryInterface,
)
from eo_lib.domain.entities import Person, Team, TeamMember, Project

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


class JsonProjectRepository(GenericJsonRepository[Project], ProjectRepositoryInterface):
    """JSON implementation of the Project Repository."""

    def __init__(self):
        super().__init__("projects.json", Project)

    def _to_obj(self, data: dict) -> Project:
        """Converts JSON dict to Project entity."""
        return Project(
            name=data["name"],
            status=data.get("status", "active"),
            id=data["id"],
            description=data.get("description"),
        )

    def _to_dict(self, project: Project) -> dict:
        """Converts Project entity to JSON dict."""
        return {
            "id": project.id,
            "name": project.name,
            "status": project.status,
            "description": project.description,
        }

    def add_team_to_project(self, project_id: int, team_id: int) -> None:
        """Stub for assigning a team in JSON mode."""
        pass

    def get_teams(self, project_id: int) -> List[Team]:
        """Stub for listing teams in JSON mode."""
        return []
