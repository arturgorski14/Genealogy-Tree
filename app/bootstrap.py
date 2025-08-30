from app.application.bus import CommandBus, QueryBus
from app.application.command_handlers import CreatePersonHandler
from app.application.commands import CreatePersonCommand
from app.application.queries import GetAllPeopleQuery, GetPersonQuery
from app.application.query_handlers import GetAllPeopleHandler, GetPersonHandler
from app.core.config import get_driver
from app.infrastructure.repository import PersonRepository


def _build_busses() -> tuple[QueryBus, CommandBus]:
    driver = get_driver()
    person_repo = PersonRepository(driver)

    query_bus = QueryBus()
    query_bus.register(GetAllPeopleQuery, GetAllPeopleHandler(person_repo))
    query_bus.register(GetPersonQuery, GetPersonHandler(person_repo))

    command_bus = CommandBus()
    command_bus.register(CreatePersonCommand, CreatePersonHandler(person_repo))

    return query_bus, command_bus


_query_bus, _command_bus = _build_busses()


def get_query_bus() -> QueryBus:
    return _query_bus


def get_command_bus() -> CommandBus:
    return _command_bus
