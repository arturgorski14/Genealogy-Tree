from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class Person(BaseModel):
    uid: UUID | None = None  # None when creating a new person
    name: str


class ParentType(StrEnum):
    father = "father"
    mother = "mother"


class ParentRelationshipInput(BaseModel):
    parent_id: UUID
    child_id: UUID
    type: ParentType


class XD(BaseModel):
    name: str
