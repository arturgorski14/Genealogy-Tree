import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.database import get_driver
from app.models import ParentRelationshipInput, Person

app = FastAPI()
driver = get_driver()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/people")
def get_all_people():
    print("Getting people")
    with driver.session() as session:
        result = session.run("MATCH (p:Person) RETURN p")
        return [record["p"] for record in result]


@app.get("/people/{person_id}")
def get_person(person_id: str):
    print("Getting person")
    with driver.session() as session:
        result = session.run(
            "MATCH (p:Person {uid: $uid}) RETURN p", uid=person_id
        )  # noqa E501
        record = result.single()
        if record:
            return record["p"]
        raise HTTPException(status_code=404, detail="Person not found")


@app.post("/people")
def create_person(person: Person):
    print("Creating person")
    with driver.session() as session:
        session.run(
            "CREATE (p:Person {uid: $uid, name: $name})",
            uid=uuid.uuid4(),
            name=person.name,
        )
    return person


@app.post("/relationships/parent")
def create_parent_relationship(rel: ParentRelationshipInput):
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
