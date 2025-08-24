from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.application.bus import QueryBus
from app.application.queries import GetAllPeopleQuery, GetPersonQuery
from app.bootstrap import get_query_bus

router = APIRouter()


@router.get("/")
def get_all_people(query_bus: QueryBus = Depends(get_query_bus)):
    return query_bus.dispatch(GetAllPeopleQuery())


@router.get("/{uid}")
def get_person(uid: str, query_bus: QueryBus = Depends(get_query_bus)):
    result = query_bus.dispatch(GetPersonQuery(uid))
    if result is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Person not found")
    return result
