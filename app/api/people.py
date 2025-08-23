from fastapi import APIRouter, Depends

from app.database import get_driver

router = APIRouter()


@router.get("/")
def get_all_people(driver=Depends(get_driver)):
    with driver.session() as session:
        result = session.run("MATCH (p:Person) RETURN p")
        return [{"uid": r["p"]["uid"], "name": r["p"]["name"]} for r in result]
