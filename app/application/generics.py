from typing import Protocol, TypeVar

"""
Variance is about where a type parameter appears (input vs output):

If a type variable appears in return position, it must be covariant.
→ “I can return a subtype safely”.

If a type variable appears in argument position, it must be contravariant.
→ “I can accept a supertype safely”.
"""


R = TypeVar("R", covariant=True)  # result type for queries and commands


class Query(Protocol[R]):
    """A query that returns a result of type R."""

    ...


class Command(Protocol[R]):
    """A command that returns R (often None)."""

    ...


Q = TypeVar("Q", bound=Query, contravariant=True)  # must be a Query[...] subclass


class QueryHandler(Protocol[Q, R]):
    def handle(self, query: Q) -> R: ...


C = TypeVar("C", bound=Command, contravariant=True)  # command result type (often None)


class CommandHandler(Protocol[C, R]):
    def handle(self, cmd: C) -> R: ...
