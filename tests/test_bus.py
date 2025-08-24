from typing import Type

import pytest

from app.application.bus import QueryBus
from app.application.queries import GetAllPeopleQuery, GetPersonQuery


class FakeHandler:
    def handle(self, query):
        return "handled"


@pytest.mark.parametrize(
    "query, query_args, query_kwargs",
    [
        (GetAllPeopleQuery, (), {}),
        (GetPersonQuery, ("uid-1234",), {}),
    ],
)
def test_query_bus_dispatches_to_handler(query: Type, query_args, query_kwargs):
    # Arrange
    bus = QueryBus()
    bus.register(query, FakeHandler())

    # Act
    result = bus.dispatch(query(*query_args, **query_kwargs))

    # Assert
    assert result == "handled"


def test_query_bus_dispatches_unregistered_query():
    # Arrange
    bus = QueryBus()

    # Act & Assert
    with pytest.raises(KeyError):
        bus.dispatch(GetAllPeopleQuery())
