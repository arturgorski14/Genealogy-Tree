from typing import Protocol, TypeVar

"""
Variance is about where a type parameter appears (input vs output):

If a type variable appears in return position, it must be covariant.
→ “I can return a subtype safely”.

If a type variable appears in argument position, it must be contravariant.
→ “I can accept a supertype safely”.
"""


RQ = TypeVar("RQ", covariant=True)  # result type for queries
RC = TypeVar("RC", covariant=True)  # result type for commands


class Query(Protocol[RQ]):
    """A query that returns a result of type R."""

    ...


class Command(Protocol[RC]):
    """A command that returns R (often None)."""

    ...


Q = TypeVar("Q", bound=Query, contravariant=True)  # must be a Query[...] subclass
C = TypeVar("C", bound=Command, contravariant=True)  # command result type (often None)


class QueryHandler(Protocol[Q, RQ]):
    def handle(self, query: Q) -> RQ: ...


class CommandHandler(Protocol[C, RC]):
    def handle(self, cmd: C) -> RC: ...
