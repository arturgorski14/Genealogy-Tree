from app.domain.person import Person
from app.infrastructure.repository import PersonRepository


def test_get_all_returns_person_objects(mocked_driver_with_data):
    repository = PersonRepository(driver=mocked_driver_with_data)
    people = repository.get_all()
    assert isinstance(people, list)
    assert all(isinstance(p, Person) for p in people)


def test_get_returns_person(mocked_driver_with_single_record):
    repository = PersonRepository(driver=mocked_driver_with_single_record)
    existing = repository.get("1")
    assert isinstance(existing, Person)


def test_get_returns_none_for_missing_uid(mocked_driver_without_data):
    repository = PersonRepository(driver=mocked_driver_without_data)
    assert repository.get("non-existent") is None


def test_create_person_object(mocked_driver_without_data):
    repository = PersonRepository(driver=mocked_driver_without_data)
    payload = {"name": "fake"}

    created = repository.create(**payload)

    assert isinstance(created, Person)
    assert created.uid is not None
