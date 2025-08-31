from typing import Type

import pytest

from app.application.bus import CommandBus, QueryBus
from app.application.commands import CreatePersonCommand
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


def test_query_bus_dispatches_unregistered_query():
    # Arrange
    bus = QueryBus()

    # Act & Assert
    with pytest.raises(
        KeyError,
        match=f"Query {GetAllPeopleQuery.__name__} not registered in {bus.__class__.__name__}.",
    ):
        bus.dispatch(GetAllPeopleQuery())


def test_command_bus_dispatches_to_handler():
    # Arrange
    command = CreatePersonCommand
    bus = CommandBus()
    bus.register(command, FakeHandler())

    # Act
    result = bus.dispatch(command("name-fake"))

    # Assert
    assert result == "handled"


def test_command_bus_dispatches_unregistered_command():
    # Arrange
    bus = CommandBus()

    # Act & Assert
    with pytest.raises(
        KeyError,
        match=f"Command {CreatePersonCommand.__name__} not registered in {bus.__class__.__name__}.",
    ):
        bus.dispatch(CreatePersonCommand("fake-name"))
