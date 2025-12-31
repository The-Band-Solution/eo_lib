"""
Domain Repository Interfaces.

Defines the contracts for data access across different storage strategies.
"""

from libbase.infrastructure.interface import IRepository as GenericRepositoryInterface
from .team_repository import TeamRepositoryInterface
from .person_repository import PersonRepositoryInterface
from .project_repository import ProjectRepositoryInterface

__all__ = [
    "TeamRepositoryInterface",
    "PersonRepositoryInterface",
    "ProjectRepositoryInterface",
    "GenericRepositoryInterface",
]
