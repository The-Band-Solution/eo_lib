import pytest
from datetime import date
from unittest.mock import MagicMock
from eo_lib.services import PersonService
from eo_lib.domain.entities import Person


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def service(mock_repo):
    return PersonService(mock_repo)


def test_create_person(service, mock_repo):
    # Arrange
    name = "Test User"
    emails = ["test@example.com"]
    ident = "ID123"
    bday = date(1990, 1, 1)
    expected_person = Person(
        name=name, emails=emails, identification_id=ident, birthday=bday, id=1
    )
    mock_repo.add.return_value = expected_person

    # Act
    result = service.create(name, emails, identification_id=ident, birthday=bday)

    # Assert
    mock_repo.add.assert_called_once()
    assert result.name == name
    assert [e.email for e in result.emails] == emails
    assert result.identification_id == ident
    assert result.birthday == bday
    assert result.id == 1


def test_get_person_found(service, mock_repo):
    person = Person(name="Alice", emails=["alice@test.com"], id=10)
    mock_repo.get_by_id.return_value = person

    result = service.get(10)
    assert result == person


def test_get_person_not_found(service, mock_repo):
    mock_repo.get_by_id.return_value = None
    with pytest.raises(ValueError, match="Person 999 not found"):
        service.get(999)


def test_update_person(service, mock_repo):
    original = Person(name="Old", emails=["old@test.com"], id=1)
    mock_repo.get_by_id.return_value = original
    mock_repo.update.return_value = None

    result = service.update(1, name="New")

    mock_repo.update.assert_called_once()
    assert result.name == "New"


def test_delete_person(service, mock_repo):
    mock_repo.delete.return_value = None
    service.delete(1)
    mock_repo.delete.assert_called_with(1)


def test_list_persons(service, mock_repo):
    p1 = Person(name="A", emails=["a@a.com"], id=1)
    p2 = Person(name="B", emails=["b@b.com"], id=2)
    mock_repo.get_all.return_value = [p1, p2]

    result = service.list()
    assert len(result) == 2
    assert result[0] == p1
    assert result[1] == p2
