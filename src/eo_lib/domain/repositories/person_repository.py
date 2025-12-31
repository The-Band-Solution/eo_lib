from eo_lib.domain.entities.person import Person
from .generic_repository import GenericRepositoryInterface

class PersonRepositoryInterface(GenericRepositoryInterface[Person]):
    """
    Interface for Person Repository.
    
    Extends GenericRepositoryInterface to provide specific data access
    operations for Person entities. Inherits standard CRUD functionality.
    """
    pass
