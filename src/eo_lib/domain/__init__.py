from .base import Base

# Generally domain exports entities and repositories, but they are in subpackages.
# To flatten: from eo_lib.domain import Person ?
# or just ensure the folder is a module.
# Let's verify what's in domain root: base.py only.
# So we export Base.
# And maybe the subpackages if we want standard access?
# usually `from eo_lib.domain.entities import Person` is fine.
# But `from eo_lib.domain import Person` is what the rule implies "reduce path".
# let's try to expose main things.

from .entities import (
    Person,
    Team,
    TeamMember,
    Initiative,
    InitiativeType,
    Organization,
    OrganizationalUnit,
    Role,
)
from .repositories import (
    PersonRepositoryInterface,
    TeamRepositoryInterface,
    InitiativeRepository,
    InitiativeTypeRepository,
    GenericRepositoryInterface,
)

__all__ = [
    "Base",
    "Person",
    "Team",
    "TeamMember",
    "Initiative",
    "InitiativeType",
    "Organization",
    "OrganizationalUnit",
    "Role",
    "PersonRepositoryInterface",
    "TeamRepositoryInterface",
    "InitiativeRepository",
    "InitiativeTypeRepository",
    "GenericRepositoryInterface",
]
