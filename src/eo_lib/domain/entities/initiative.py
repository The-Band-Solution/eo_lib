from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from eo_lib.domain.base import Base
from typing import List, Optional

# Forward reference for association tables
initiative_teams = Table(
    "initiative_teams",
    Base.metadata,
    Column("initiative_id", Integer, ForeignKey("initiatives.id"), primary_key=True),
    Column("team_id", Integer, ForeignKey("teams.id"), primary_key=True),
)

initiative_persons = Table(
    "initiative_persons",
    Base.metadata,
    Column("initiative_id", Integer, ForeignKey("initiatives.id"), primary_key=True),
    Column("person_id", Integer, ForeignKey("persons.id"), primary_key=True),
)


class InitiativeType(Base):
    """
    InitiativeType Model.

    Categorizes Initiatives (e.g., 'Strategic', 'Operational', 'Research').
    """

    __tablename__ = "initiative_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    initiatives = relationship("Initiative", back_populates="initiative_type")

    def __init__(
        self, name: str, description: Optional[str] = None, id: Optional[int] = None
    ):
        if id:
            self.id = id
        self.name = name
        self.description = description


class Initiative(Base):
    """
    Initiative Model (formerly Project).

    Represents a planned undertaking within an Organization. Initiatives can have
    hierarchical structures (sub-initiatives), types, and involve multiple Teams and Persons.

    Attributes:
        id (int): Unique identifier.
        name (str): Unique name of the initiative.
        status (str): Current status (e.g., 'active').
        description (str): Optional description.
        start_date (datetime): Start date.
        end_date (datetime): End date.
        initiative_type_id (int): Link to InitiativeType.
        organization_id (int): Link to Organization.
        parent_id (int): Link to parent Initiative.
    """

    __tablename__ = "initiatives"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, default="active", index=True)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=True, index=True)
    end_date = Column(DateTime, nullable=True, index=True)

    initiative_type_id = Column(
        Integer, ForeignKey("initiative_types.id"), index=True, nullable=True
    )
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    parent_id = Column(Integer, ForeignKey("initiatives.id"), nullable=True)

    # Relationships
    initiative_type = relationship("InitiativeType", back_populates="initiatives")
    organization = relationship("Organization", back_populates="initiatives")
    parent = relationship(
        "Initiative", remote_side=[id], back_populates="sub_initiatives"
    )
    sub_initiatives = relationship("Initiative", back_populates="parent")
    teams = relationship(
        "Team", secondary=initiative_teams, back_populates="initiatives", lazy="joined"
    )
    persons = relationship(
        "Person", secondary=initiative_persons, back_populates="initiatives"
    )

    def __init__(
        self,
        name: str,
        status: str = "active",
        description: Optional[str] = None,
        start_date: Optional[DateTime] = None,
        end_date: Optional[DateTime] = None,
        initiative_type_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        parent_id: Optional[int] = None,
        id: Optional[int] = None,
    ):
        if id:
            self.id = id
        self.name = name
        self.status = status
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.initiative_type_id = initiative_type_id
        self.organization_id = organization_id
        self.parent_id = parent_id
