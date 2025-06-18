import uuid

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.database import get_driver
from app.models import Person

router = APIRouter()


@router.get("/")
def get_all_people(driver=Depends(get_driver)):
    with driver.session() as session:
        result = session.run("MATCH (p:Person) RETURN p")
        return [{"uid": r["p"]["uid"], "name": r["p"]["name"]} for r in result]


@router.get("/{person_id}")
def get_person(person_id: str, driver=Depends(get_driver)):
    with driver.session() as session:
        result = session.run(
            "MATCH (p:Person {uid: $uid}) RETURN p", uid=person_id
        )  # noqa E501
        record = result.single()
        if record:
            return {"uid": record["p"]["uid"], "name": record["p"]["name"]}
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Person not found")


@router.post("/")
def create_person(person: Person, driver=Depends(get_driver)):
    with driver.session() as session:
        uid = str(uuid.uuid4())
        session.run(
            "CREATE (p:Person {uid: $uid, name: $name})",
            uid=uid,
            name=person.name,
        )
    return {"uid": uid, "name": person.name}


@router.delete("/{person_id}")
def delete_person(person_id: str, driver=Depends(get_driver)):
    with driver.session() as session:
        result = session.run(
            "MATCH (p:Person {uid: $uid}) DELETE p RETURN COUNT(p) AS deleted_count",
            uid=person_id,
        )
        deleted_count = result.single().get("deleted_count")
        if deleted_count == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Person not found")

        if deleted_count > 1:  # TODO: make this case redundant, by adding a constraint
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Multiple people deleted — data integrity issue",
            )
    return {"message": f"Person {person_id} deleted successfully"}
