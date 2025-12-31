from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from eo_lib.domain.base import Base
from typing import List, Optional

# Forward reference for association table
project_teams = Table(
    'project_teams', Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True)
)

class Project(Base):
    """
    Unified Project Model.
    Represents both Domain Entity and Database Table.
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, default="active")
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)

    # Relationships
    teams = relationship("Team", secondary=project_teams, back_populates="projects")

    def __init__(self, name: str, status: str = "active", description: str = None, start_date = None, end_date = None, id: Optional[int] = None):
        """
        Initialize Project.
        
        Args:
            name (str): The name of the project.
            status (str): Current status (default: 'active').
            description (str): Detailed description.
            start_date (datetime): Start date.
            end_date (datetime): End date.
            id (int, optional): Database ID.
        """
        self.name = name
        self.status = status
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        if id: self.id = id
