from typing import List, Optional
from datetime import datetime
from eo_lib.domain.entities import Initiative, InitiativeType, Team
from eo_lib.domain.repositories import (
    InitiativeRepository,
    InitiativeTypeRepository,
    TeamRepositoryInterface,
)


class InitiativeService:
    def __init__(
        self,
        initiative_repo: InitiativeRepository,
        initiative_type_repo: InitiativeTypeRepository,
        team_repo: TeamRepositoryInterface,
    ):
        self.initiative_repo = initiative_repo
        self.initiative_type_repo = initiative_type_repo
        self.team_repo = team_repo

    def create_initiative(
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
        return self.initiative_repo.add(initiative)

    def get_initiative(self, initiative_id: int) -> Optional[Initiative]:
        return self.initiative_repo.get(initiative_id)

    def list_initiatives(self) -> List[Initiative]:
        return self.initiative_repo.list()

    def create_initiative_type(
        self, name: str, description: Optional[str] = None
    ) -> InitiativeType:
        existing = self.initiative_type_repo.get_by_name(name)
        if existing:
            raise ValueError(f"InitiativeType '{name}' already exists")

        new_type = InitiativeType(name=name, description=description)
        return self.initiative_type_repo.add(new_type)

    def list_initiative_types(self) -> List[InitiativeType]:
        return self.initiative_type_repo.list()

    def update_initiative(
        self,
        initiative_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        initiative_type_name: Optional[str] = None,
    ) -> Initiative:
        initiative = self.initiative_repo.get(initiative_id)
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

        return self.initiative_repo.update(initiative)

    def assign_team(self, initiative_id: int, team_id: int) -> None:
        initiative = self.initiative_repo.get(initiative_id)
        if not initiative:
            raise ValueError(f"Initiative {initiative_id} not found")

        team = self.team_repo.get(team_id)
        if not team:
            raise ValueError(f"Team {team_id} not found")

        # Check if already assigned to avoid duplicates if necessary
        # Assuming list check or set behavior. SQLAlchemy handles duplicates in list usually by appending.
        # Check if team in initiative.teams
        if any(t.id == team.id for t in initiative.teams):
            return  # Already assigned

        initiative.teams.append(team)
        self.initiative_repo.update(initiative)

    def get_teams(self, initiative_id: int) -> List[Team]:
        initiative = self.initiative_repo.get(initiative_id)
        if not initiative:
            raise ValueError(f"Initiative {initiative_id} not found")
        return initiative.teams
