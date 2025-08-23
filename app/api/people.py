from fastapi import APIRouter, Depends

from app.application.bus import QueryBus
from app.application.queries import GetAllPeopleQuery
from app.bootstrap import get_query_bus

router = APIRouter()


@router.get("/")
def get_all_people(query_bus: QueryBus = Depends(get_query_bus)):
    return query_bus.dispatch(GetAllPeopleQuery())
