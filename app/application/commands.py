from dataclasses import dataclass


@dataclass
class CreatePersonCommand:
    name: str
