from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from eo_lib.domain.base import Base
from eo_lib.domain.entities.initiative import initiative_persons
from typing import Optional, List
from datetime import date


class Person(Base):
    """
    Person Model.

    Represents an individual within the system. A Person can belong to multiple
    Organizations, work on multiple Initiatives, and be a member of various Teams.

    Attributes:
        id (int): Unique identifier (Primary Key).
        name (str): Full name of the person.
        identification_id (str): Unique identification number (e.g., SSN, Tax ID).
        birthday (date): Date of birth.
        organizations (relationship): Many-to-many relationship with Organization entities.
        initiatives (relationship): Many-to-many relationship with Initiative entities.
        emails (relationship): One-to-many relationship with PersonEmail entities.
        memberships (relationship): One-to-many relationship with TeamMember associations.
    """

    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    identification_id = Column(String, unique=True, index=True, nullable=True)
    birthday = Column(Date, nullable=True)

    # Relationships
    organizations = relationship(
        "Organization", secondary="organization_persons", back_populates="persons"
    )
    initiatives = relationship(
        "Initiative", secondary=initiative_persons, back_populates="persons"
    )
    emails = relationship(
        "PersonEmail",
        back_populates="person",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    memberships = relationship(
        "TeamMember", back_populates="person", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        name: str,
        emails: Optional[List[str]] = None,
        identification_id: Optional[str] = None,
        birthday: Optional[date] = None,
        organizations: Optional[List] = None,
        id: Optional[int] = None,
    ):
        """
        Initializes a new Person instance.

        Args:
            name (str): The full name of the person.
            emails (List[str], optional): A list of email addresses associated with the person. Defaults to None.
            identification_id (str, optional): A unique identification string. Defaults to None.
            birthday (date, optional): The person's date of birth. Defaults to None.
            organizations (List[Organization], optional): Initial list of Organizations the person belongs to. Defaults to None.
            id (int, optional): Database ID for existing records. Defaults to None.
        """
        self.name = name
        self.identification_id = identification_id
        self.birthday = birthday
        if organizations:
            self.organizations = organizations
        if emails:
            self.emails = [PersonEmail(email=e) for e in emails]
        if id:
            self.id = id


class PersonEmail(Base):
    """
    PersonEmail Model.

    Represents an email address associated with a specific Person.
    Supports multiple emails per Person.

    Attributes:
        id (int): Unique identifier (Primary Key).
        person_id (int): Foreign Key linking to the owner Person.
        email (str): The email address (unique).
        person (relationship): Relationship to the owner Person.
    """

    __tablename__ = "person_emails"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    person = relationship("Person", back_populates="emails")

    def __init__(
        self, email: str, person_id: Optional[int] = None, id: Optional[int] = None
    ):
        """
        Initializes a new PersonEmail instance.

        Args:
            email (str): The email address string.
            person_id (int, optional): The ID of the Person this email belongs to. Defaults to None.
            id (int, optional): Database ID for existing records. Defaults to None.
        """
        self.email = email
        if person_id:
            self.person_id = person_id
        if id:
            self.id = id
