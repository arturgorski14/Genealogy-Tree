import pytest

from app.application.queries import GetAllPeopleQuery, GetPersonQuery
from app.application.query_handlers import GetAllPeopleHandler, GetPersonHandler
from tests.fakes import FakeRepository


def test_get_all_people_handler_delegates():
    repo = FakeRepository()
    handler = GetAllPeopleHandler(repo)
    query = GetAllPeopleQuery()

    handler.handle(query)

    assert repo._called_method == "get_all"


@pytest.mark.parametrize("uid", ["1", "non-existent"])
def test_get_person_handler_delegates(uid):
    repo = FakeRepository()
    handler = GetPersonHandler(repo)
    query = GetPersonQuery(uid)

    handler.handle(query)

    assert repo._called_method == "get"
    assert repo._called_args == uid
