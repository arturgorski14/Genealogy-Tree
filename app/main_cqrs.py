from app.application.bus import QueryBus
from app.application.queries import GetAllPeopleQuery
from app.application.query_handlers import GetAllPeopleHandler
from app.core.config import get_driver
from app.infrastructure.repository import PeopleRepository

query_bus = QueryBus()
repo = PeopleRepository(get_driver())
query_bus.register(GetAllPeopleQuery, GetAllPeopleHandler(repo))

people = query_bus.dispatch(GetAllPeopleQuery())
print(len(people))
print(people)
