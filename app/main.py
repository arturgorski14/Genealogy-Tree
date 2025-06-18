from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import people
from app.database import get_driver
from app.models import ParentRelationshipInput

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(people.router, prefix="/people", tags=["people"])


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
