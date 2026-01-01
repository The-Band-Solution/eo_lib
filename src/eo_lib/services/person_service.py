from typing import List
from eo_lib.domain.repositories import PersonRepositoryInterface
from eo_lib.domain.entities import Person, PersonEmail
from libbase.services.generic_service import GenericService
from datetime import date


class PersonService(GenericService[Person]):
    """
    Service for managing Person-related business logic.
    Inherits generic CRUD operations from GenericService.
    """

    def __init__(self, repo: PersonRepositoryInterface):
        """
        Initializes the PersonService with a specific repository.
        """
        super().__init__(repo)
        self.repo = repo  # type alias for typed access if needed, though _repository exists

    def create_with_details(
        self,
        name: str,
        emails: List[str] = None,
        identification_id: str = None,
        birthday: date = None,
    ) -> Person:
        """
        Creates and stores a new Person using detail arguments.
        Wraps the generic create(entity) method.
        """
        person = Person(
            name=name,
            emails=emails,
            identification_id=identification_id,
            birthday=birthday,
        )
        self.create(person)
        return person

    def update_details(
        self,
        id: int,
        name: str = None,
        emails: List[str] = None,
        identification_id: str = None,
        birthday: date = None,
    ) -> Person:
        """
        Updates an existing Person's information finding it by ID first.
        """
        p = self.get_by_id(id)
        if not p:
            raise ValueError(f"Person {id} not found")
            
        if name:
            p.name = name
        if identification_id:
            p.identification_id = identification_id
        if birthday:
            p.birthday = birthday
        if emails is not None:
            p.emails = [PersonEmail(email=e) for e in emails]
            
        self.update(p)
        return p
