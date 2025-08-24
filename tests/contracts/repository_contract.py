import pytest

from app.domain.person import Person


class PersonRepositoryContract:
    """
    Tests that must pass for *any* PersonRepository implementation.
    """

    @pytest.mark.contract
    def test_get_all_returns_person_objects(self, repository):
        people = repository.get_all()
        assert isinstance(people, list)
        assert all(isinstance(p, Person) for p in people)

    @pytest.mark.contract
    def test_get_returns_person(self, repository):
        existing = repository.get("1")
        if existing is not None:
            assert isinstance(existing, Person)

    @pytest.mark.contract
    def test_get_returns_none_for_missing_uid(self, repository):
        assert repository.get("non-existent") is None
