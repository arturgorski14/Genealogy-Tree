from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.api.request_schemas import AddParentChildRequest, CreatePersonRequest
from app.application.bus import CommandBus, QueryBus
from app.application.commands import (
    AddParentChildRelationCommand,
    CreatePersonCommand,
    DeletePersonCommand,
)
from app.application.queries import GetAllPeopleQuery, GetPersonQuery
from app.bootstrap import get_command_bus, get_query_bus

router = APIRouter()


@router.get("/")
def get_all_people(
    query_bus: QueryBus = Depends(get_query_bus),
):  # TODO: add sorting, limits and offset
    return query_bus.dispatch(GetAllPeopleQuery())


@router.get("/{uid}")
def get_person(uid: str, query_bus: QueryBus = Depends(get_query_bus)):
    result = query_bus.dispatch(GetPersonQuery(uid))
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Person {uid} not found"
        )
    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_person(
    body: CreatePersonRequest, command_bus: CommandBus = Depends(get_command_bus)
):
    result = command_bus.dispatch(CreatePersonCommand(body.name))
    return result


@router.post("/relationships/parent-child", status_code=status.HTTP_201_CREATED)
def add_parent_child(
    body: AddParentChildRequest,
    command_bus: CommandBus = Depends(get_command_bus),
):
    created = command_bus.dispatch(
        AddParentChildRelationCommand(body.parent_id, body.child_id)
    )
    if not created:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Cycle detected"
        )
    return {"status": "relationship_created"}


@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(uid: str, bus: CommandBus = Depends(get_command_bus)):
    success = bus.dispatch(DeletePersonCommand(uid))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Person {uid} not found"
        )
