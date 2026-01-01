import pytest
from unittest.mock import MagicMock
from datetime import date
from eo_lib.services import TeamService
from eo_lib.domain.entities import Team, TeamMember


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def service(mock_repo):
    return TeamService(mock_repo)


def test_create_team(service, mock_repo):
    t = Team(name="A-Team", description="Heroes", id=1)
    
    def simulate_add(team):
        team.id = 1
        return None
        
    mock_repo.add.side_effect = simulate_add

    # create -> create_team (wrapper)
    result = service.create_team("A-Team", "Heroes")

    mock_repo.add.assert_called_once()
    assert result.name == "A-Team"


def test_get_team(service, mock_repo):
    t = Team(name="A", id=1)
    mock_repo.get_by_id.return_value = t
    # get -> get_by_id
    assert service.get_by_id(1) == t


def test_get_team_not_found(service, mock_repo):
    mock_repo.get_by_id.return_value = None
    # GenericService.get_by_id returns None usually.
    # We update expectation.
    assert service.get_by_id(99) is None
    # with pytest.raises(ValueError):
    #     service.get(99)


def test_update_team(service, mock_repo):
    orig = Team(name="Old", id=1)
    mock_repo.get_by_id.return_value = orig

    # update -> update_team_details
    service.update_team_details(1, name="New")
    mock_repo.update.assert_called_once()


def test_delete_team(service, mock_repo):
    mock_repo.delete.return_value = None
    service.delete(1)
    mock_repo.delete.assert_called_with(1)


def test_list_teams(service, mock_repo):
    mock_repo.get_all.return_value = []
    # list -> get_all
    assert service.get_all() == []


def test_add_member(service, mock_repo):
    mock_role = MagicMock()
    mock_role.name = "Lead"
    tm = TeamMember(person_id=1, team_id=1, role=mock_role, id=10)
    mock_repo.add_member.return_value = tm

    today = date.today()
    result = service.add_member(1, 1, role=mock_role, start_date=today)

    mock_repo.add_member.assert_called_once()
    assert result.role.name == "Lead"


def test_remove_member(service, mock_repo):
    mock_repo.remove_member.return_value = True
    service.remove_member(10)
    mock_repo.remove_member.assert_called_with(10)


def test_get_members(service, mock_repo):
    mock_repo.get_members.return_value = []
    assert service.get_members(1) == []
