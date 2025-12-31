from typing import List
from eo_lib.factories import ServiceFactory
from eo_lib.domain.entities.person import Person
from datetime import date

class PersonController:
    """
    Facade for Person operations.
    Exposes simple API for creation, retrieval, updates, and deletion.
    """
    def __init__(self): 
        """Initialize Service."""
        self.service = ServiceFactory.create_person_service()

    def create_person(self, name: str, emails: List[str] = None, identification_id: str = None, birthday: date = None) -> Person: 
        """
        Create a new person.
        
        Args:
            name (str): Person Name.
            emails (List[str]): Person Emails.
            identification_id (str): Unique ID.
            birthday (date): Birthday.
            
        Returns:
            Person: The object.
        """
        return self.service.create(name, emails, identification_id, birthday)
    def get_person(self, id: int) -> Person: 
        """Get person by ID."""
        return self.service.get(id)
    def update_person(self, id: int, name: str = None, emails: List[str] = None, identification_id: str = None, birthday: date = None) -> Person: 
        return self.service.update(id, name, emails, identification_id, birthday)
    def delete_person(self, id: int) -> None: self.service.delete(id)
    def list_persons(self) -> List[Person]: return self.service.list()
