from eo_lib.domain.entities import Organization
from libbase.infrastructure.interface import IRepository as GenericRepositoryInterface


class OrganizationRepositoryInterface(GenericRepositoryInterface[Organization]):
    """
    Interface for Organization Repository.
    """
    pass
