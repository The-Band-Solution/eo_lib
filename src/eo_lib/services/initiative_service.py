from typing import List, Optional
from datetime import datetime
from eo_lib.domain.entities import Initiative, InitiativeType, Team
from eo_lib.domain.repositories import (
    InitiativeRepository,
    InitiativeTypeRepository,
    TeamRepositoryInterface,
)
from libbase.services.generic_service import GenericService


class InitiativeService(GenericService[Initiative]):
    def __init__(
        self,
        initiative_repo: InitiativeRepository,
        initiative_type_repo: InitiativeTypeRepository,
        team_repo: TeamRepositoryInterface,
    ):
        super().__init__(initiative_repo)
        # Using self.repo (from parent) for initiative_repo if generic access is needed
        self.initiative_repo = initiative_repo 
        self.initiative_type_repo = initiative_type_repo
        self.team_repo = team_repo

    def create_initiative_with_details(
        self,
        name: str,
        description: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        initiative_type_name: Optional[str] = None,
    ) -> Initiative:
        # Resolve Initiative Type if provided
        initiative_type_id = None
        if initiative_type_name:
            itype = self.initiative_type_repo.get_by_name(initiative_type_name)
            if itype:
                initiative_type_id = itype.id
            else:
                raise ValueError(f"InitiativeType '{initiative_type_name}' not found")

        initiative = Initiative(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            initiative_type_id=initiative_type_id,
        )
        self.create(initiative)
        return initiative

    def create_initiative_type(
        self, name: str, description: Optional[str] = None
    ) -> InitiativeType:
        existing = self.initiative_type_repo.get_by_name(name)
        if existing:
            raise ValueError(f"InitiativeType '{name}' already exists")

        new_type = InitiativeType(name=name, description=description)
        self.initiative_type_repo.add(new_type)
        return new_type

    def list_initiative_types(self) -> List[InitiativeType]:
        return self.initiative_type_repo.get_all()

    def update_initiative_details(
        self,
        initiative_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        initiative_type_name: Optional[str] = None,
    ) -> Initiative:
        initiative = self.get_by_id(initiative_id)
        if not initiative:
            raise ValueError(f"Initiative {initiative_id} not found")

        if name:
            initiative.name = name
        if description:
            initiative.description = description
        if status:
            initiative.status = status
        if start_date:
            initiative.start_date = start_date
        if end_date:
            initiative.end_date = end_date

        if initiative_type_name:
            itype = self.initiative_type_repo.get_by_name(initiative_type_name)
            if itype:
                initiative.initiative_type_id = itype.id
            else:
                raise ValueError(f"InitiativeType '{initiative_type_name}' not found")

        self.update(initiative)
        return initiative

    def assign_team(self, initiative_id: int, team_id: int) -> None:
        initiative = self.get_by_id(initiative_id)
        if not initiative:
            raise ValueError(f"Initiative {initiative_id} not found")

        team = self.team_repo.get_by_id(team_id)
        if not team:
            raise ValueError(f"Team {team_id} not found")

        # Check if already assigned to avoid duplicates
        if any(t.id == team.id for t in initiative.teams):
            return  # Already assigned

        initiative.teams.append(team)
        self.update(initiative)

    def get_teams(self, initiative_id: int) -> List[Team]:
        initiative = self.get_by_id(initiative_id)
        if not initiative:
            raise ValueError(f"Initiative {initiative_id} not found")
        return initiative.teams
