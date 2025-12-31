from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from eo_lib.domain.base import Base
from typing import List, Optional

# Association table for Organization <-> Person Many-to-Many
organization_persons = Table(
    "organization_persons",
    Base.metadata,
    Column(
        "organization_id", Integer, ForeignKey("organizations.id"), primary_key=True
    ),
    Column("person_id", Integer, ForeignKey("persons.id"), primary_key=True),
)


class Organization(Base):
    """
    Organization Model.

    Represents a formal organization that serves as the root container for
    other domain entities such as Projects, Teams, and Organizational Units.

    Attributes:
        id (int): Unique identifier (Primary Key).
        name (str): Unique name of the organization.
        description (str): Optional text description.
        short_name (str): Optional abbreviated name for the organization.
        persons (relationship): Many-to-many relationship with Person entities.
        projects (relationship): One-to-many relationship with Project entities.
        teams (relationship): One-to-many relationship with Team entities.
        units (relationship): One-to-many relationship with OrganizationalUnit entities.
    """

    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    short_name = Column(String, index=True, nullable=True)

    # Relationships
    persons = relationship(
        "Person", secondary=organization_persons, back_populates="organizations"
    )
    initiatives = relationship(
        "Initiative", back_populates="organization", cascade="all, delete-orphan"
    )
    teams = relationship(
        "Team", back_populates="organization", cascade="all, delete-orphan"
    )
    units = relationship(
        "OrganizationalUnit",
        back_populates="organization",
        cascade="all, delete-orphan",
    )

    def __init__(
        self,
        name: str,
        description: str = None,
        short_name: str = None,
        id: Optional[int] = None,
    ):
        """
        Initializes a new Organization instance.

        Args:
            name (str): The name of the organization.
            description (str, optional): A brief summary of the organization. Defaults to None.
            short_name (str, optional): A short identifier or acronym. Defaults to None.
            id (int, optional): Database ID for existing records. Defaults to None.
        """
        self.name = name
        self.description = description
        self.short_name = short_name
        if id:
            self.id = id
