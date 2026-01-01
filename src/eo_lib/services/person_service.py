from typing import List
from eo_lib.domain.repositories import PersonRepositoryInterface
from eo_lib.domain.entities import Person
from datetime import date


class PersonService:
    """
    Service for managing Person-related business logic.

    Provides high-level operations for creating, retrieving, updating,
    and deleting Persons, abstracting the underlying repository interactions.
    """

    def __init__(self, repo: PersonRepositoryInterface):
        """
        Initializes the PersonService with a specific repository.

        Args:
            repo (PersonRepositoryInterface): The repository implementation for data access.
        """
        self.repo = repo

    def create(
        self,
        name: str,
        emails: List[str] = None,
        identification_id: str = None,
        birthday: date = None,
    ) -> Person:
        """
        Creates and stores a new Person.

        Args:
            name (str): The full name of the person.
            emails (List[str], optional): Initial list of email addresses. Defaults to None.
            identification_id (str, optional): Unique ID string. Defaults to None.
            birthday (date, optional): Birth date. Defaults to None.

        Returns:
            Person: The newly created and stored Person entity.
        """
        person = Person(
            name=name,
            emails=emails,
            identification_id=identification_id,
            birthday=birthday,
        )
        self.repo.add(person)
        return person

    def get(self, id: int) -> Person:
        """
        Retrieves a Person by their unique identifier.

        Args:
            id (int): The ID of the Person to retrieve.

        Returns:
            Person: The retrieved Person entity.

        Raises:
            ValueError: If no Person is found with the given ID.
        """
        p = self.repo.get_by_id(id)
        if not p:
            raise ValueError(f"Person {id} not found")
        return p

    def update(
        self,
        id: int,
        name: str = None,
        emails: List[str] = None,
        identification_id: str = None,
        birthday: date = None,
    ) -> Person:
        """
        Updates an existing Person's information.

        Args:
            id (int): ID of the Person to update.
            name (str, optional): New name. Defaults to None.
            emails (List[str], optional): New list of email addresses. Defaults to None.
            identification_id (str, optional): New identification ID. Defaults to None.
            birthday (date, optional): New birthday. Defaults to None.

        Returns:
            Person: The updated Person entity.

        Raises:
            ValueError: If no Person is found with the given ID.
        """
        from eo_lib.domain.entities import PersonEmail

        p = self.get(id)
        if name:
            p.name = name
        if identification_id:
            p.identification_id = identification_id
        if birthday:
            p.birthday = birthday
        if emails is not None:
            p.emails = [PersonEmail(email=e) for e in emails]
        self.repo.update(p)
        return p

    def delete(self, id: int) -> None:
        """
        Deletes a Person from the system.

        Args:
            id (int): ID of the Person to delete.

        Raises:
            ValueError: If no Person is found with the given ID.
        """
        self.repo.delete(id)

    def list(self) -> List[Person]:
        """
        Retrieves a list of all Persons in the system.

        Returns:
            List[Person]: A list containing all Person entities.
        """
        return self.repo.get_all()
