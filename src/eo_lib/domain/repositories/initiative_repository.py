from eo_lib.domain.entities.initiative import Initiative
from libbase.infrastructure.interface import IRepository as GenericRepositoryInterface


class InitiativeRepository(GenericRepositoryInterface[Initiative]):
    """
    Interface for Initiative Repository.

    Extends GenericRepositoryInterface to provide specific data access
    operations for Initiative entities. Inherits standard CRUD functionality.
    """
    pass
