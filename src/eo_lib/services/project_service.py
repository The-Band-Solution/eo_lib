from typing import List
from eo_lib.domain.repositories import ProjectRepositoryInterface
from eo_lib.domain.entities import Project, Team


class ProjectService:
    """
    Service for managing Project-related business logic.

    Provides high-level operations for creating, retrieving, updating,
    and deleting Projects, as well as managing team assignments to projects.
    """

    def __init__(self, repo: ProjectRepositoryInterface):
        """
        Initializes the ProjectService with a specific repository.

        Args:
            repo (ProjectRepositoryInterface): The repository implementation for data access.
        """
        self.repo = repo

    def create(
        self, name: str, description: str = None, start_date=None, end_date=None
    ) -> Project:
        """
        Creates and stores a new Project.

        Args:
            name (str): The name of the project.
            description (str, optional): A brief summary of the project. Defaults to None.
            start_date (datetime, optional): The scheduled start date. Defaults to None.
            end_date (datetime, optional): The scheduled end date. Defaults to None.

        Returns:
            Project: The newly created and stored Project entity.
        """
        project = Project(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
        )
        self.repo.add(project)
        return project

    def get(self, id: int) -> Project:
        """
        Retrieves a Project by its unique identifier.

        Args:
            id (int): The ID of the Project to retrieve.

        Returns:
            Project: The retrieved Project entity.

        Raises:
            ValueError: If no Project is found with the given ID.
        """
        p = self.repo.get_by_id(id)
        if not p:
            raise ValueError(f"Project {id} not found")
        return p

    def update(
        self,
        id: int,
        name: str = None,
        status: str = None,
        description: str = None,
        start_date=None,
        end_date=None,
    ) -> Project:
        """
        Updates an existing Project's information.

        Args:
            id (int): ID of the Project to update.
            name (str, optional): New name. Defaults to None.
            status (str, optional): New status. Defaults to None.
            description (str, optional): New description. Defaults to None.
            start_date (datetime, optional): New start date. Defaults to None.
            end_date (datetime, optional): New end date. Defaults to None.

        Returns:
            Project: The updated Project entity.

        Raises:
            ValueError: If no Project is found with the given ID.
        """
        p = self.get(id)
        if name:
            p.name = name
        if status:
            p.status = status
        if description:
            p.description = description
        if start_date:
            p.start_date = start_date
        if end_date:
            p.end_date = end_date
        self.repo.update(p)
        return p

    def delete(self, id: int) -> None:
        """
        Deletes a Project from the system.

        Args:
            id (int): ID of the Project to delete.

        Raises:
            ValueError: If no Project is found with the given ID.
        """
        self.repo.delete(id)

    def list(self) -> List[Project]:
        """
        Retrieves a list of all Projects in the system.

        Returns:
            List[Project]: A list containing all Project entities.
        """
        return self.repo.get_all()

    def assign_team(self, project_id: int, team_id: int):
        """
        Assigns a Team to work on a specific Project.

        Args:
            project_id (int): The ID of the Project.
            team_id (int): The ID of the Team to assign.
        """
        self.repo.add_team_to_project(project_id, team_id)

    def get_teams(self, project_id: int) -> List[Team]:
        """
        Retrieves all Teams assigned to a specific Project.

        Args:
            project_id (int): The ID of the Project.

        Returns:
            List[Team]: A list of assigned Team entities.
        """
        return self.repo.get_teams(project_id)
