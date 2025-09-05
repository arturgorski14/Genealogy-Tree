from neo4j.exceptions import ServiceUnavailable

from app.application.bus import CommandBus, QueryBus
from app.application.command_handlers import CreatePersonHandler, DeletePersonHandler
from app.application.commands import CreatePersonCommand, DeletePersonCommand
from app.application.queries import GetAllPeopleQuery, GetPersonQuery
from app.application.query_handlers import GetAllPeopleHandler, GetPersonHandler
from app.core.config import get_driver
from app.domain.person import Person
from app.infrastructure.repository import PersonRepository


def check_neo4j():
    driver = get_driver()
    try:
        with driver.session() as session:
            result = session.run("RETURN 1 AS ok").single()
            return result["ok"] == 1
    except ServiceUnavailable as e:
        print("Neo4j is not reachable:", e)
        return False


if not check_neo4j():
    print("⚠️ Neo4j is NOT running or credentials are wrong")
    exit(1)


person_repo = PersonRepository(get_driver())

query_bus = QueryBus()
query_bus.register(GetAllPeopleQuery, GetAllPeopleHandler(person_repo))
query_bus.register(GetPersonQuery, GetPersonHandler(person_repo))

people = query_bus.dispatch(GetAllPeopleQuery())
print(len(people))
print(people)

person_uid = people[0].uid
print(f"{person_uid=}")
person = query_bus.dispatch(GetPersonQuery(person_uid))
print(f"{person=}")

command_bus = CommandBus()
command_bus.register(CreatePersonCommand, CreatePersonHandler(person_repo))
command_bus.register(DeletePersonCommand, DeletePersonHandler(person_repo))

new_person: Person = command_bus.dispatch(CreatePersonCommand("new-person"))
print(new_person)
deleted = command_bus.dispatch(DeletePersonCommand(new_person.uid))
print(deleted)
