from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from eo_lib.domain.base import Base
from eo_lib.domain.entities.initiative import initiative_teams
from datetime import date
from typing import Optional


class Team(Base):
    """
    Team Model.

    Represents a collaborative group of Persons within an Organization.
    Teams are assigned to Initiatives and have specific Members with defined Roles.

    Attributes:
        id (int): Unique identifier (Primary Key).
        name (str): Unique name of the team.
        description (str): Optional text description.
        short_name (str): Optional abbreviated name for the team.
        organization_id (int): Foreign Key linking to the parent Organization.
        organization (relationship): Relationship to the parent Organization.
        members (relationship): One-to-many relationship with TeamMember associations.
        initiatives (relationship): many-to-many relationship with Initiative entities.
    """

    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    short_name = Column(String, index=True, nullable=True)

    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)

    # Relationships
    organization = relationship("Organization", back_populates="teams")
    members = relationship(
        "TeamMember", back_populates="team", cascade="all, delete-orphan", lazy="joined"
    )
    initiatives = relationship(
        "Initiative", secondary=initiative_teams, back_populates="teams"
    )

    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        short_name: Optional[str] = None,
        organization_id: Optional[int] = None,
        id: Optional[int] = None,
    ):
        """
        Initializes a new Team instance.

        Args:
            name (str): Unique name for the team.
            description (str, optional): A brief summary of the team's purpose. Defaults to None.
            short_name (str, optional): A short identifier or acronym. Defaults to None.
            organization_id (int, optional): Link to the Organization this team belongs to. Defaults to None.
            id (int, optional): Database ID for existing records. Defaults to None.
        """
        self.name = name
        self.description = description
        self.short_name = short_name
        self.organization_id = organization_id
        if id:
            self.id = id


class TeamMember(Base):
    """
    TeamMember Model.

    An association table representing the participation of a Person in a Team.
    Includes additional relationship metadata such as Role and participation dates.

    Attributes:
        id (int): Unique identifier (Primary Key).
        person_id (int): Foreign Key linking to the participant Person.
        team_id (int): Foreign Key linking to the parent Team.
        role_id (int): Foreign Key linking to the Person's Role in the Team.
        start_date (datetime): When the Person joined the team.
        end_date (datetime): When the Person left the team (if applicable).
        person (relationship): Relationship to the participant Person.
        team (relationship): Relationship to the parent Team.
        role (relationship): Relationship to the defined Role.
    """

    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime, nullable=True)

    # Relationships
    person = relationship("Person", back_populates="memberships", lazy="joined")
    team = relationship("Team", back_populates="members")
    role = relationship("Role", back_populates="team_memberships", lazy="joined")

    def __init__(
        self,
        person_id: int,
        team_id: int,
        role_id: Optional[int] = None,
        role: Optional[object] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        id: Optional[int] = None,
    ):
        """
        Initializes a new TeamMember association.

        Args:
            person_id (int): ID of the Person joining the team.
            team_id (int): ID of the Team being joined.
            role_id (int, optional): ID of the Role assigned to the person. Defaults to None.
            role (Role or str, optional): Role object or Role name as string. Defaults to None.
            start_date (date, optional): Date when membership begins. Defaults to None.
            end_date (date, optional): Date when membership ends. Defaults to None.
            id (int, optional): Database ID for existing records. Defaults to None.
        """
        self.person_id = person_id
        self.team_id = team_id
        self.role_id = role_id
        if role:
            if isinstance(role, str):
                from eo_lib.domain.entities.role import Role

                self.role = Role(name=role)
            else:
                self.role = role
        self.start_date = start_date
        self.end_date = end_date
        if id:
            self.id = id
