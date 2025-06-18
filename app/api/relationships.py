from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.database import get_driver
from app.models import ParentRelationshipInput

router = APIRouter()


@router.post("/parent")
def create_parent_relationship(
    rel: ParentRelationshipInput, driver=Depends(get_driver)
):
    with driver.session() as session:
        session.run(
            "MATCH (child:Person {uid: $child_id}), (parent:Person {uid: $parent_id})"
            " MERGE (parent)-[r:PARENT]->(child)"
            " SET r.type = $type",
            parent_id=str(rel.parent_id),
            child_id=str(rel.child_id),
            type=rel.type.value,
        )
    return {
        "message": f"Parent relationship between {str(rel.parent_id)}->{str(rel.child_id)} created"  # noqa E501
    }


@router.get("/")
def get_all_relationships(driver=Depends(get_driver)):
    with driver.session() as session:
        result = session.run(
            "MATCH (parent:Person)-[r:PARENT]->(child:Person)"
            " RETURN parent.uid AS parent_id, child.uid AS child_id, r.type AS type"
        )
        return [
            {"parent_id": r["parent_id"], "child_id": r["child_id"], "type": r["type"]}
            for r in result
        ]


@router.delete("/{parent_id}/{child_id}")
def delete_parent_relationship(
    parent_id: str, child_id: str, driver=Depends(get_driver)
):
    with driver.session() as session:
        result = session.run(
            "MATCH (parent:Person {uid: $parent_id})-[r:PARENT]"
            "->(child:Person {uid: $child_id})"
            " DELETE r RETURN count(r) AS deleted_count",
            parent_id=parent_id,
            child_id=child_id,
        )
        deleted_count = result.single()["deleted_count"]
        if deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parent relationship between {parent_id}->{child_id} not found",
            )
    return {"message": f"Parent relationship between {parent_id}->{child_id} deleted"}


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
