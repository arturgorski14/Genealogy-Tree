import pytest

from app.application.queries import GetAllPeopleQuery, GetPersonQuery
from app.application.query_handlers import GetAllPeopleHandler, GetPersonHandler
from tests.fakes import FakeRepository


def test_get_all_people_handler_delegates():
    # Arrange
    repo = FakeRepository()
    handler = GetAllPeopleHandler(repo)
    query = GetAllPeopleQuery()

    # Act
    handler.handle(query)

    # Assert
    assert repo._called_method == "get_all"


@pytest.mark.parametrize("uid", ["1", "non-existent"])
def test_get_person_handler_delegates(uid):
    # Arrange
    repo = FakeRepository()
    handler = GetPersonHandler(repo)
    query = GetPersonQuery(uid)

    # Act
    handler.handle(query)

    # Assert
    assert repo._called_method == "get"
    assert repo._called_args == uid
