from typing import Protocol, TypeVar

R = TypeVar("R", covariant=True)  # result type for queries


class Query(Protocol[R]):
    """A query that returns a result of type R."""

    ...


C = TypeVar("C", covariant=True)  # command result type (often None)


class Command(Protocol[C]):
    """A command that returns C (often None)."""

    ...
