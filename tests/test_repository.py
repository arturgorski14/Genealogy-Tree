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


# TODO: tests
"""
- successful deletion
- deletion of non existent person
"""
