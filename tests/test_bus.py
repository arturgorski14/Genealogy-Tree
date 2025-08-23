from app.application.bus import QueryBus
from app.application.queries import GetAllPeopleQuery


class FakeHandler:
    def handle(self, query):
        return "handled"


def test_query_bus_dispatches_to_handler():
    bus = QueryBus()
    bus.register(GetAllPeopleQuery, FakeHandler())

    result = bus.dispatch(GetAllPeopleQuery())

    assert result == "handled"
