from unittest.mock import MagicMock

from app.domain.person import Person
from app.infrastructure.repository import PeopleRepository, PersonRepository


def mock_neo4j_driver_with_session(mock_records=None, single_record=None):
    """
    Mocks a Neo4j driver with a session, returning
    mock_records for iteration
    single_record for .single()
    """
    mock_session = MagicMock()
    mock_session.run.return_value = MagicMock(
        __iter__=lambda self: iter(mock_records or []),
        single=MagicMock(return_value=single_record),
    )
    mock_driver = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    return mock_driver, mock_session


def test_get_all_people_returns_list():
    # Arrange
    mock_records = [
        {"p": {"uid": "1", "name": "Alice"}},
        {"p": {"uid": "2", "name": "Bob"}},
    ]
    mock_driver, _ = mock_neo4j_driver_with_session(mock_records=mock_records)
    repo = PeopleRepository(mock_driver)

    # Act
    result: list[Person] = repo.get_all()
    # Assert
    assert len(result) == 2
    assert result[0].uid == "1"
    assert result[0].name == "Alice"
    assert result[1].uid == "2"
    assert result[1].name == "Bob"


def test_get_person():
    # Arrange
    uid = "1"
    name = "Alice"
    single_record = {"p": {"uid": uid, "name": name}}
    mock_driver, _ = mock_neo4j_driver_with_session(single_record=single_record)
    repo = PersonRepository(mock_driver)

    # Act
    result = repo.get(uid)

    # Assert
    assert result.uid == uid
    assert result.name == name


def test_get_person_with_invalid_uid():
    # Arrange
    uid = "non-existent-uid"
    mock_driver, _ = mock_neo4j_driver_with_session(single_record=None)
    repo = PersonRepository(mock_driver)
    # Act
    result = repo.get(uid)

    # Assert
    assert result is None
