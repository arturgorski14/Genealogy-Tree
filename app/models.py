from pydantic import BaseModel


class Person(BaseModel):
    id: str | None = None  # optional for POST
    name: str
