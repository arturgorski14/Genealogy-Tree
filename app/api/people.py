from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.api.request_schemas import CreatePersonRequest
from app.application.bus import CommandBus, QueryBus
from app.application.commands import CreatePersonCommand
from app.application.queries import GetAllPeopleQuery, GetPersonQuery
from app.bootstrap import get_command_bus, get_query_bus

router = APIRouter()


@router.get("/")
def get_all_people(query_bus: QueryBus = Depends(get_query_bus)):
    return query_bus.dispatch(GetAllPeopleQuery())


@router.get("/{uid}")
def get_person(uid: str, query_bus: QueryBus = Depends(get_query_bus)):
    result = query_bus.dispatch(GetPersonQuery(uid))
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Person not found"
        )
    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_person(
    body: CreatePersonRequest, command_bus: CommandBus = Depends(get_command_bus)
):
    result = command_bus.dispatch(CreatePersonCommand(body.name))
    return result
