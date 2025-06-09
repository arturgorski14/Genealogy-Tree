from pydantic import BaseModel


class Person(BaseModel):
    uid: str | None = None  # should be None in POST
    name: str
