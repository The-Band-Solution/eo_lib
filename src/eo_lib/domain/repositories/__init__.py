"""
Domain Repository Interfaces.

Defines the contracts for data access across different storage strategies.
"""

from libbase.infrastructure.interface import IRepository as GenericRepositoryInterface
from .team_repository import TeamRepositoryInterface
from .person_repository import PersonRepositoryInterface
from .initiative_repository import InitiativeRepository
from .initiative_type_repository import InitiativeTypeRepository

__all__ = [
    "TeamRepositoryInterface",
    "PersonRepositoryInterface",
    "InitiativeRepository",
    "InitiativeTypeRepository",
    "GenericRepositoryInterface",
]
