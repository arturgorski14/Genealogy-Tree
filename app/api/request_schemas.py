from pydantic import BaseModel


class CreatePersonRequest(BaseModel):
    name: str


class AddParentChildRequest(BaseModel):
    parent_id: str
    child_id: str
