from app.application.bus import QueryBus
from app.application.queries import GetAllPeopleQuery, GetPersonQuery
from app.application.query_handlers import GetAllPeopleHandler, GetPersonHandler
from app.core.config import get_driver
from app.infrastructure.repository import PeopleRepository, PersonRepository

people_repo = PeopleRepository(get_driver())
person_repo = PersonRepository(get_driver())

query_bus = QueryBus()
query_bus.register(GetAllPeopleQuery, GetAllPeopleHandler(people_repo))
query_bus.register(GetPersonQuery, GetPersonHandler(person_repo))

people = query_bus.dispatch(GetAllPeopleQuery())
print(len(people))
print(people)

person_uid = people[0]["uid"]
print(f"{person_uid=}")
person = query_bus.dispatch(GetPersonQuery(person_uid))
print(f"{person=}")
