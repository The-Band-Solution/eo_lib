import pytest
from unittest.mock import MagicMock
from datetime import date
from eo_lib.services.team_service import TeamService
from eo_lib.domain.entities.team import Team, TeamMember

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return TeamService(mock_repo)

def test_create_team(service, mock_repo):
    t = Team(name="A-Team", description="Heroes", id=1)
    mock_repo.add.return_value = t
    
    result = service.create("A-Team", "Heroes")
    
    mock_repo.add.assert_called_once()
    assert result.name == "A-Team"

def test_get_team(service, mock_repo):
    t = Team(name="A", id=1)
    mock_repo.get.return_value = t
    assert service.get(1) == t

def test_get_team_not_found(service, mock_repo):
    mock_repo.get.return_value = None
    with pytest.raises(ValueError):
        service.get(99)

def test_update_team(service, mock_repo):
    orig = Team(name="Old", id=1)
    mock_repo.get.return_value = orig
    
    service.update(1, name="New")
    mock_repo.update.assert_called_once()

def test_delete_team(service, mock_repo):
    mock_repo.delete.return_value = True
    service.delete(1)
    mock_repo.delete.assert_called_with(1)

def test_list_teams(service, mock_repo):
    mock_repo.list.return_value = []
    assert service.list() == []

def test_add_member(service, mock_repo):
    tm = TeamMember(person_id=1, team_id=1, role="Lead", id=10)
    mock_repo.add_member.return_value = tm
    
    today = date.today()
    result = service.add_member(1, 1, "Lead", start_date=today)
    
    mock_repo.add_member.assert_called_once()
    assert result.role == "Lead"

def test_remove_member(service, mock_repo):
    mock_repo.remove_member.return_value = True
    service.remove_member(10)
    mock_repo.remove_member.assert_called_with(10)

def test_get_members(service, mock_repo):
    mock_repo.get_members.return_value = []
    assert service.get_members(1) == []
