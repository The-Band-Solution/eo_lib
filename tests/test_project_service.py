import pytest
from unittest.mock import MagicMock
from eo_lib.services.project_service import ProjectService
from eo_lib.domain.entities.project import Project
from eo_lib.domain.entities.team import Team

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return ProjectService(mock_repo)

def test_create_project(service, mock_repo):
    p = Project(name="Mars", id=1)
    mock_repo.add.return_value = p
    assert service.create("Mars") == p

def test_get_project(service, mock_repo):
    p = Project(name="Mars", id=1)
    mock_repo.get.return_value = p
    assert service.get(1) == p

def test_update_project(service, mock_repo):
    orig = Project(name="Mars", id=1)
    mock_repo.get.return_value = orig
    service.update(1, status="Done")
    mock_repo.update.assert_called_once()

def test_delete_project(service, mock_repo):
    mock_repo.delete.return_value = True
    service.delete(1)
    mock_repo.delete.assert_called_with(1)

def test_list_projects(service, mock_repo):
    mock_repo.list.return_value = []
    assert service.list() == []

def test_assign_team(service, mock_repo):
    service.assign_team(1, 2)
    mock_repo.add_team_to_project.assert_called_with(1, 2)

def test_get_teams(service, mock_repo):
    t = Team(name="A", id=2)
    mock_repo.get_teams.return_value = [t]
    result = service.get_teams(1)
    assert len(result) == 1
    assert result[0] == t
