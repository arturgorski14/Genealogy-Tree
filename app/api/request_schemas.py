from pydantic import BaseModel


class CreatePersonRequest(BaseModel):
    name: str
