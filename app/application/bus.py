from typing import Type

from app.application.generics import Command, CommandHandler, Query, QueryHandler


class QueryBus:
    def __init__(self):
        self._handlers: dict[Type[Query], QueryHandler] = {}

    def register(self, query_type: Type[Query], handler: QueryHandler):
        self._handlers[query_type] = handler

    def dispatch(self, query: Query):
        handler = self._handlers[type(query)]
        return handler.handle(query)


class CommandBus:
    def __init__(self):
        self._handlers: dict[Type[Command], CommandHandler] = {}

    def register(self, command_type: Type[Command], handler: CommandHandler) -> None:
        self._handlers[command_type] = handler

    def dispatch(self, command: Command):
        handler = self._handlers[type(command)]
        return handler.handle(command)
