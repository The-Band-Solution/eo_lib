from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from eo_lib.domain.base import Base
from typing import Optional


class Role(Base):
    """
    Role Model.

    Represents a specific functional role or position a Person can occupy within a Team.
    Roles help define responsibilities and access levels within projects and organizations.

    Attributes:
        id (int): Unique identifier (Primary Key).
        name (str): Unique name of the role (e.g., 'Lead', 'Developer', 'Designer').
        description (str): Optional text description of the role's responsibilities.
        team_memberships (relationship): relationship to the TeamMember associations.
    """

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    team_memberships = relationship("TeamMember", back_populates="role")

    def __init__(self, name: str, description: str = None, id: Optional[int] = None):
        """
        Initializes a new Role instance.

        Args:
            name (str): Unique role name.
            description (str, optional): A detailed description of the role's purpose. Defaults to None.
            id (int, optional): Database ID for existing records. Defaults to None.
        """
        self.name = name
        self.description = description
        if id:
            self.id = id
