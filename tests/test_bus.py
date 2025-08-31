from typing import Type

import pytest

from app.application.bus import CommandBus, QueryBus
from app.application.commands import CreatePersonCommand
from app.application.exceptions import HandlerNotRegistered
from app.application.queries import GetAllPeopleQuery, GetPersonQuery
from app.application.query_handlers import FakeHandler


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


def test_command_bus_dispatches_to_handler():
    # Arrange
    command = CreatePersonCommand
    bus = CommandBus()
    bus.register(command, FakeHandler())

    # Act
    result = bus.dispatch(command("name-fake"))

    # Assert
    assert result == "handled"


@pytest.mark.parametrize(
    "bus_cls, msg, obj",
    [
        (
            QueryBus,
            "Query GetAllPeopleQuery not registered in QueryBus",
            GetAllPeopleQuery(),
        ),
        (
            CommandBus,
            "Command CreatePersonCommand not registered in CommandBus",
            CreatePersonCommand("name-fake"),
        ),
    ],
)
def test_dispatch_unregistered_raises(bus_cls, msg, obj):
    bus = bus_cls()
    with pytest.raises(HandlerNotRegistered, match=msg):
        bus.dispatch(obj)
