from typing import List
from eo_lib.factories import ServiceFactory
from eo_lib.domain.entities.person import Person
from datetime import date


class PersonController:
    """
    Controller for Person-related operations.

    Acts as a facade for the PersonService, providing a simple and clean API
    for external consumers to manage Persons and their associated data.
    """

    def __init__(self):
        """Initializes the Controller by creating the required PersonService."""
        self.service = ServiceFactory.create_person_service()

    def create_person(
        self,
        name: str,
        emails: List[str] = None,
        identification_id: str = None,
        birthday: date = None,
    ) -> Person:
        """
        Creates a new person record.

        Args:
            name (str): The full name of the person.
            emails (List[str], optional): List of email addresses. Defaults to None.
            identification_id (str, optional): Unique ID string. Defaults to None.
            birthday (date, optional): Date of birth. Defaults to None.

        Returns:
            Person: The newly created Person entity.
        """
        return self.service.create(name, emails, identification_id, birthday)

    def get_person(self, id: int) -> Person:
        """
        Retrieves a person by their ID.

        Args:
            id (int): The unique ID of the person.

        Returns:
            Person: The person entity.
        """
        return self.service.get(id)

    def update_person(
        self,
        id: int,
        name: str = None,
        emails: List[str] = None,
        identification_id: str = None,
        birthday: date = None,
    ) -> Person:
        """
        Updates an existing person's details.

        Args:
            id (int): ID of the person to update.
            name (str, optional): Updated name. Defaults to None.
            emails (List[str], optional): Updated list of emails. Defaults to None.
            identification_id (str, optional): Updated ID string. Defaults to None.
            birthday (date, optional): Updated birthday. Defaults to None.

        Returns:
            Person: The updated Person entity.
        """
        return self.service.update(id, name, emails, identification_id, birthday)

    def delete_person(self, id: int) -> None:
        """
        Deletes a person record.

        Args:
            id (int): ID of the person to delete.
        """
        self.service.delete(id)

    def list_persons(self) -> List[Person]:
        """
        Retrieves all person records.

        Returns:
            List[Person]: A list of all Person entities.
        """
        return self.service.list()
