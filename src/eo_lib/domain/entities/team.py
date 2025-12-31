from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from eo_lib.domain.base import Base
from eo_lib.domain.entities.project import project_teams
from datetime import date
from typing import Optional

class Team(Base):
    """
    Unified Team Model.
    Represents a group of people.
    """
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
    projects = relationship("Project", secondary=project_teams, back_populates="teams")

    def __init__(self, name: str, description: str = None, id: Optional[int] = None):
        """
        Initialize Team.
        
        Args:
            name (str): Unique team name.
            description (str, optional): Description.
            id (int, optional): DB ID.
        """
        self.name = name
        self.description = description
        if id: self.id = id

class TeamMember(Base):
    """
    Unified TeamMember Model.
    Association table with extra attributes for Person-Team relationship.
    """
    __tablename__ = "team_members"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    role = Column(String, default="member")
    start_date = Column(DateTime, default=func.now()) 
    end_date = Column(DateTime, nullable=True)

    # Relationships
    person = relationship("Person", back_populates="memberships")
    team = relationship("Team", back_populates="members")

    def __init__(self, person_id: int, team_id: int, role: str, start_date: date = None, end_date: date = None, id: Optional[int] = None):
        """
        Initialize Team Member.
        
        Args:
            person_id (int): ID of person.
            team_id (int): ID of team.
            role (str): Role in team.
            start_date (date): Start.
            end_date (date): End.
            id (int): DB ID.
        """
        self.person_id = person_id
        self.team_id = team_id
        self.role = role
        self.start_date = start_date
        self.end_date = end_date
        if id: self.id = id
