import pytest

from app.domain.person import Person
from app.infrastructure.repository import PersonRepository
from tests.conftest import mock_neo4j_driver_with_session


def test_get_all_returns_person_objects(mocked_driver_with_data):
    # Arrange
    repository = PersonRepository(driver=mocked_driver_with_data)

    # Act
    people = repository.get_all()

    # Assert
    assert isinstance(people, list)
    assert len(people) > 0
    assert all(isinstance(p, Person) for p in people)


def test_get_returns_person(mocked_driver_with_single_record):
    # Arrange
    repository = PersonRepository(driver=mocked_driver_with_single_record)

    # Act
    existing = repository.get("1")

    # Assert
    assert isinstance(existing, Person)
    assert existing.uid == "1"


def test_get_returns_none_for_missing_uid(mocked_driver_without_data):
    # Arrange
    repository = PersonRepository(driver=mocked_driver_without_data)

    # Act & Assert
    assert repository.get("non-existent") is None


def test_create_person_object():
    # Arrange
    single_record = {"p": {"uid": "fake-uid", "name": "fake"}}
    driver, _ = mock_neo4j_driver_with_session(single_record=single_record)
    repository = PersonRepository(driver=driver)

    # Act
    created = repository.create(name="fake")

    # Assert
    assert isinstance(created, Person)
    assert created.uid == "fake-uid"
    assert created.name == "fake"


def test_delete_existing_person_returns_true():
    single_record = {"deleted_count": 1}
    driver, _ = mock_neo4j_driver_with_session(single_record=single_record)
    repo = PersonRepository(driver=driver)

    assert repo.delete("1") is True


def test_delete_nonexistent_person_returns_false(mocked_driver_without_data):
    repo = PersonRepository(driver=mocked_driver_without_data)

    result = repo.delete("does-not-exist")

    assert result is False


def test_add_parent_child_creates_relationship():
    driver, mock_session = mock_neo4j_driver_with_session()
    repo = PersonRepository(driver=driver)

    repo.add_parent_child("p1", "c1")

    mock_session.run.assert_called_once()
    cypher, params = mock_session.run.call_args[0][0], mock_session.run.call_args[1]
    assert "PARENT" in cypher
    assert params["parent_id"] == "p1"
    assert params["child_id"] == "c1"


@pytest.mark.skip(reason="Not implemented yet")
def test_add_parent_child_dont_create_relationship_if_its_already_exist(): ...
