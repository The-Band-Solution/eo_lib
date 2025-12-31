"""
Domain Repository Interfaces.

Defines the contracts for data access across different storage strategies.
"""
from .team_repository import TeamRepositoryInterface
from .person_repository import PersonRepositoryInterface
from .project_repository import ProjectRepositoryInterface
from .generic_repository import GenericRepositoryInterface

__all__ = [
    "TeamRepositoryInterface",
    "PersonRepositoryInterface",
    "ProjectRepositoryInterface",
    "GenericRepositoryInterface",
]
