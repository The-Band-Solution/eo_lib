from typing import List
from eo_lib.domain.repositories.person_repository import PersonRepositoryInterface
from eo_lib.domain.entities.person import Person
from datetime import date

class PersonService:
    """
    Business logic for Person management.
    """
    def __init__(self, repo: PersonRepositoryInterface): 
        """
        Initialize with Repository.
        
        Args:
            repo (PersonRepositoryInterface): Data access layer.
        """
        self.repo = repo
    
    def create(self, name: str, emails: List[str] = None, identification_id: str = None, birthday: date = None) -> Person: 
        """
        Create a new person.
        
        Args:
            name (str): Person's name.
            emails (List[str]): List of emails.
            identification_id (str): Unique ID.
            birthday (date): Birthday.
            
        Returns:
            Person: Created entity.
        """
        return self.repo.add(Person(name=name, emails=emails, identification_id=identification_id, birthday=birthday))
    
    def get(self, id: int) -> Person: 
        """
        Get person by ID.
        
        Raises:
            ValueError: If not found.
        """
        p = self.repo.get(id)
        if not p: raise ValueError(f"Person {id} not found")
        return p

    def update(self, id: int, name: str = None, emails: List[str] = None, identification_id: str = None, birthday: date = None) -> Person:
        from eo_lib.domain.entities.person import PersonEmail
        p = self.get(id)
        if name: p.name = name
        if identification_id: p.identification_id = identification_id
        if birthday: p.birthday = birthday
        if emails is not None:
            p.emails = [PersonEmail(email=e) for e in emails]
        return self.repo.update(p)

    def delete(self, id: int) -> None:
        if not self.repo.delete(id): raise ValueError(f"Person {id} not found")

    def list(self) -> List[Person]:
        return self.repo.list()
