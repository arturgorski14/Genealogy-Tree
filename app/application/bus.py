from app.application.generics import Command, Query


class QueryBus:
    def __init__(self):
        self._handlers = {}

    def register(self, query_type, handler):
        self._handlers[query_type] = handler

    def dispatch(self, query: Query):
        handler = self._handlers[type(query)]
        return handler.handle(query)


class CommandBus:
    def __init__(self):
        self._handlers = {}

    def register(self, command_type, handler) -> None:
        self._handlers[command_type] = handler

    def dispatch(self, command: Command):
        handler = self._handlers[type(command)]
        return handler.handle(command)
