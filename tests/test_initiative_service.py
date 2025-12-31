import pytest
from unittest.mock import MagicMock
from eo_lib.services.initiative_service import InitiativeService
from eo_lib.domain.entities import Initiative, Team, InitiativeType


@pytest.fixture
def mock_initiative_repo():
    return MagicMock()


@pytest.fixture
def mock_type_repo():
    return MagicMock()


@pytest.fixture
def mock_team_repo():
    return MagicMock()


@pytest.fixture
def service(mock_initiative_repo, mock_type_repo, mock_team_repo):
    return InitiativeService(mock_initiative_repo, mock_type_repo, mock_team_repo)


def test_create_initiative(service, mock_initiative_repo):
    p = Initiative(name="Mars", id=1)
    mock_initiative_repo.add.return_value = p
    created = service.create_initiative("Mars")
    assert created == p
    mock_initiative_repo.add.assert_called()


def test_create_initiative_with_type(service, mock_initiative_repo, mock_type_repo):
    p = Initiative(name="Mars", id=1, initiative_type_id=10)
    itype = InitiativeType(id=10, name="Space")
    mock_type_repo.get_by_name.return_value = itype
    mock_initiative_repo.add.return_value = p

    created = service.create_initiative("Mars", initiative_type_name="Space")
    assert created.initiative_type_id == 10
    mock_type_repo.get_by_name.assert_called_with("Space")


def test_get_initiative(service, mock_initiative_repo):
    p = Initiative(name="Mars", id=1)
    mock_initiative_repo.get.return_value = p
    assert service.get_initiative(1) == p
    mock_initiative_repo.get.assert_called_with(1)


def test_update_initiative(service, mock_initiative_repo):
    orig = Initiative(name="Mars", id=1)
    mock_initiative_repo.get.return_value = orig
    mock_initiative_repo.update.return_value = orig

    service.update_initiative(1, status="Done")

    start_args, _ = mock_initiative_repo.update.call_args
    updated_obj = start_args[0]
    assert updated_obj.status == "Done"


def test_list_initiatives(service, mock_initiative_repo):
    mock_initiative_repo.list.return_value = []
    assert service.list_initiatives() == []


def test_assign_team(service, mock_initiative_repo, mock_team_repo):
    init = Initiative(name="Mars", id=1)
    team = Team(name="A", id=2)

    mock_initiative_repo.get.return_value = init
    mock_team_repo.get.return_value = team

    service.assign_team(1, 2)

    assert team in init.teams
    mock_initiative_repo.update.assert_called_with(init)


def test_get_teams(service, mock_initiative_repo):
    init = Initiative(name="Mars", id=1)
    team = Team(name="A", id=2)
    init.teams.append(team)

    mock_initiative_repo.get.return_value = init

    teams = service.get_teams(1)
    assert len(teams) == 1
    assert teams[0] == team
