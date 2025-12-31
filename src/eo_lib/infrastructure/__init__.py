# Expose database client and repositories if needed
# Typically infrastructure exports repositories.
from .repositories import (
    GenericPostgresRepository,
    PostgresPersonRepository,
    PostgresTeamRepository,
    PostgresInitiativeRepository,
    PostgresInitiativeTypeRepository,
    InMemoryPersonRepository,
    InMemoryTeamRepository,
    InMemoryInitiativeRepository,
    InMemoryInitiativeTypeRepository,
    JsonPersonRepository,
    JsonTeamRepository,
    JsonInitiativeRepository,
    JsonInitiativeTypeRepository,
)
from .database import PostgresClient

__all__ = [
    "GenericPostgresRepository",
    "PostgresPersonRepository",
    "PostgresTeamRepository",
    "PostgresInitiativeRepository",
    "PostgresInitiativeTypeRepository",
    "InMemoryPersonRepository",
    "InMemoryTeamRepository",
    "InMemoryInitiativeRepository",
    "InMemoryInitiativeTypeRepository",
    "JsonPersonRepository",
    "JsonTeamRepository",
    "JsonInitiativeRepository",
    "JsonInitiativeTypeRepository",
    "PostgresClient",
]
