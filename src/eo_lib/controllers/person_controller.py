from typing import List
from eo_lib.factories import ServiceFactory
from eo_lib.domain.entities.person import Person
from libbase.controllers.generic_controller import GenericController
from datetime import date


class PersonController(GenericController[Person]):
    """
    Controller for Person-related operations.
    Inherits generic operations from GenericController.
    """

    def __init__(self):
        """Initializes the Controller by creating the required PersonService."""
        service = ServiceFactory.create_person_service()
        super().__init__(service)

    def create_person(
        self,
        name: str,
        emails: List[str] = None,
        identification_id: str = None,
        birthday: date = None,
    ) -> Person:
        """
        Creates a new person record.
        Wraps the service's create_with_details method.
        """
        # GenericController.create takes an entity.
        # We use the specific service method here which handles construction.
        return self._service.create_with_details(name, emails, identification_id, birthday)

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
        Wraps the service's update_details method.
        """
        return self._service.update_details(id, name, emails, identification_id, birthday)
