from eo_lib.domain.entities import OrganizationalUnit
from libbase.infrastructure.interface import IRepository as GenericRepositoryInterface


class OrganizationalUnitRepositoryInterface(GenericRepositoryInterface[OrganizationalUnit]):
    """
    Interface for Organizational Unit Repository.
    """
    pass
