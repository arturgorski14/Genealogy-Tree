from dataclasses import dataclass


@dataclass
class GetAllPeopleQuery:
    pass  # no fields needed since we want all users


@dataclass
class GetPersonQuery:
    uid: str
