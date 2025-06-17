import uuid

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.database import get_driver
from app.models import ParentRelationshipInput, Person

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/people")
def get_all_people(driver=Depends(get_driver)):
    with driver.session() as session:
        result = session.run("MATCH (p:Person) RETURN p")
        return [{"uid": r["p"]["uid"], "name": r["p"]["name"]} for r in result]


@app.get("/people/{person_id}")
def get_person(person_id: str, driver=Depends(get_driver)):
    with driver.session() as session:
        result = session.run(
            "MATCH (p:Person {uid: $uid}) RETURN p", uid=person_id
        )  # noqa E501
        record = result.single()
        if record:
            return {"uid": record["p"]["uid"], "name": record["p"]["name"]}
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Person not found")


@app.post("/people")
def create_person(person: Person, driver=Depends(get_driver)):
    with driver.session() as session:
        uid = str(uuid.uuid4())
        session.run(
            "CREATE (p:Person {uid: $uid, name: $name})",
            uid=uid,
            name=person.name,
        )
    return {"uid": uid, "name": person.name}


@app.delete("/people/{person_id}")
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


@app.post("/relationships/parent")
def create_parent_relationship(
    rel: ParentRelationshipInput, driver=Depends(get_driver)
):
    with driver.session() as session:
        session.run(
            """
            MATCH (child:Person {uid: $child_id}), (parent:Person {uid: $parent_id})
            MERGE (parent)-[r:PARENT]->(child)
            SET r.type = $type
            """,
            parent_id=str(rel.parent_id),
            child_id=str(rel.child_id),
            type=rel.type.value,
        )
    return {"message": "Parent relationship created"}


"""
Query to get person parents

MATCH (parent:Person)-[r:PARENT]->(child:Person {uid: $child_id})
RETURN parent, r.type AS relationship_type

Query to get person children

MATCH (parent:Person {uid: $parent_id})-[r:PARENT]->(child:Person)
RETURN child, r.type AS relationship_type

Query to get all people and all types of relationships in table form

MATCH (p1:Person)-[r]->(p2:Person)
RETURN p1.uid AS from_uid, p1.name AS from_name,
       type(r) AS relationship,
       r.type AS relationship_type,
       p2.uid AS to_uid, p2.name AS to_name
"""
