from app.application.bus import QueryBus
from app.application.queries import GetAllPeopleQuery
from app.application.query_handlers import GetAllPeopleHandler
from app.core.config import get_driver
from app.infrastructure.repository import PeopleRepository


def _build_query_bus() -> QueryBus:
    driver = get_driver()
    people_repo = PeopleRepository(driver)
    query_bus = QueryBus()
    query_bus.register(GetAllPeopleQuery, GetAllPeopleHandler(people_repo))
    return query_bus


_query_bus = _build_query_bus()


def get_query_bus() -> QueryBus:
    return _query_bus
