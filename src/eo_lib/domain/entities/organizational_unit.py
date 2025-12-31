from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from eo_lib.domain.base import Base
from typing import List, Optional


class OrganizationalUnit(Base):
    """
    Organizational Unit Model.

    Represents a division, department, or any functional unit within an Organization.
    Organizational Units support recursive hierarchies, allowing for the representation
    of complex corporate structures.

    Attributes:
        id (int): Unique identifier (Primary Key).
        name (str): Name of the unit.
        description (str): Optional text description.
        short_name (str): Optional abbreviated name for the unit.
        organization_id (int): Foreign Key linking to the parent Organization.
        parent_id (int): Foreign Key linking to a parent OrganizationalUnit (for recursion).
        organization (relationship): Relationship to the parent Organization.
        parent (relationship): Relationship to the parent OrganizationalUnit.
        children (relationship): Relationship to child OrganizationalUnits.
    """

    __tablename__ = "organizational_units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    short_name = Column(String, index=True, nullable=True)

    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("organizational_units.id"), nullable=True)

    # Relationships
    organization = relationship("Organization", back_populates="units")
    parent = relationship(
        "OrganizationalUnit", remote_side=[id], back_populates="children"
    )
    children = relationship("OrganizationalUnit", back_populates="parent")

    def __init__(
        self,
        name: str,
        organization_id: int,
        description: str = None,
        short_name: str = None,
        parent_id: Optional[int] = None,
        id: Optional[int] = None,
    ):
        """
        Initializes a new OrganizationalUnit instance.

        Args:
            name (str): The name of the unit.
            organization_id (int): Link to the organization the unit belongs to.
            description (str, optional): A brief summary of the unit. Defaults to None.
            short_name (str, optional): A short identifier or acronym. Defaults to None.
            parent_id (int, optional): Link to a parent unit for hierarchical structures. Defaults to None.
            id (int, optional): Database ID for existing records. Defaults to None.
        """
        self.name = name
        self.organization_id = organization_id
        self.description = description
        self.short_name = short_name
        self.parent_id = parent_id
        if id:
            self.id = id
