from eo_lib.domain.entities.person import Person
from eo_lib.domain.repositories.generic_repository import GenericRepositoryInterface

class PersonRepositoryInterface(GenericRepositoryInterface[Person]):
    """
    Interface for Person Repository.
    Inherits standard CRUD from GenericRepositoryInterface.
    """
    pass
