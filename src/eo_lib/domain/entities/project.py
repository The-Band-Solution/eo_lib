from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from eo_lib.domain.base import Base
from typing import List, Optional

# Forward reference for association tables
project_teams = Table(
    'project_teams', Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True)
)

project_persons = Table(
    'project_persons', Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('person_id', Integer, ForeignKey('persons.id'), primary_key=True)
)

class Project(Base):
    """
    Project Model.
    
    Represents a planned undertaking within an Organization. Projects can have
    hierarchical structures (sub-projects), and involve multiple Teams and Persons.
    
    Attributes:
        id (int): Unique identifier (Primary Key).
        name (str): Unique name of the project.
        status (str): Current status of the project (e.g., 'active', 'completed').
        description (str): Optional text description.
        start_date (datetime): Optional project start date.
        end_date (datetime): Optional project end date.
        organization_id (int): Foreign Key linking to the parent Organization.
        parent_id (int): Foreign Key linking to a parent Project (for recursion).
        organization (relationship): Relationship to the parent Organization.
        parent (relationship): Relationship to the parent Project.
        sub_projects (relationship): Relationship to sub-projects.
        teams (relationship): Many-to-many relationship with Team entities.
        persons (relationship): Many-to-many relationship with Person entities.
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, default="active")
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=True)
    parent_id = Column(Integer, ForeignKey('projects.id'), nullable=True)

    # Relationships
    organization = relationship("Organization", back_populates="projects")
    parent = relationship("Project", remote_side=[id], back_populates="sub_projects")
    sub_projects = relationship("Project", back_populates="parent")
    teams = relationship("Team", secondary=project_teams, back_populates="projects", lazy="joined")
    persons = relationship("Person", secondary=project_persons, back_populates="projects")

    def __init__(self, name: str, status: str = "active", description: str = None, start_date = None, end_date = None, organization_id: Optional[int] = None, parent_id: Optional[int] = None, id: Optional[int] = None):
        """
        Initializes a new Project instance.
        
        Args:
            name (str): The name of the project.
            status (str): The current status of the project. Defaults to "active".
            description (str, optional): A brief summary of the project goals. Defaults to None.
            start_date (datetime, optional): The scheduled start date. Defaults to None.
            end_date (datetime, optional): The scheduled end date. Defaults to None.
            organization_id (int, optional): Link to the Organization this project belongs to. Defaults to None.
            parent_id (int, optional): Link to a parent Project for hierarchical structures. Defaults to None.
            id (int, optional): Database ID for existing records. Defaults to None.
        """
        self.name = name
        self.status = status
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.organization_id = organization_id
        self.parent_id = parent_id
        if id: self.id = id
