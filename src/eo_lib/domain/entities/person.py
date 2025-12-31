from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from eo_lib.domain.base import Base
from typing import Optional, List
from datetime import date

class Person(Base):
    """
    Unified Person Model.
    Represents an individual in the system.
    """
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    identification_id = Column(String, unique=True, index=True, nullable=True)
    birthday = Column(Date, nullable=True)
    
    # Relationships
    emails = relationship("PersonEmail", back_populates="person", cascade="all, delete-orphan", lazy="joined")
    memberships = relationship("TeamMember", back_populates="person", cascade="all, delete-orphan")

    def __init__(self, name: str, emails: List[str] = None, identification_id: str = None, birthday: date = None, id: Optional[int] = None):
        """
        Initialize Person.
        
        Args:
            name (str): Full name.
            emails (List[str], optional): List of email addresses.
            identification_id (str, optional): Unique ID.
            birthday (date, optional): Birth date.
            id (int, optional): DB ID.
        """
        self.name = name
        self.identification_id = identification_id
        self.birthday = birthday
        if emails:
            self.emails = [PersonEmail(email=e) for e in emails]
        if id: self.id = id

class PersonEmail(Base):
    """
    Model for Person's emails.
    """
    __tablename__ = "person_emails"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    person = relationship("Person", back_populates="emails")

    def __init__(self, email: str, person_id: int = None, id: Optional[int] = None):
        self.email = email
        if person_id: self.person_id = person_id
        if id: self.id = id
