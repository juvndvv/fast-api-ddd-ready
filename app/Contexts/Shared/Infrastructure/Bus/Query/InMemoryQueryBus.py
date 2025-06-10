import logging
from typing import Any

from injector import Injector, inject, singleton

from app.Contexts.Shared.Application.Bus.Query.Query import Query
from app.Contexts.Shared.Application.Bus.Query.QueryBus import QueryBus
from app.Contexts.Shared.Application.Bus.Query.QueryHandler import QueryHandler


@singleton
class InMemoryQueryBus(QueryBus):
    _logger: logging.Logger = logging.getLogger(__name__)

    @inject
    def __init__(self, injector: Injector) -> None:
        self._injector = injector
        self._handlers: dict[type[Query], type[QueryHandler]] = {}

    def ask(self, query: Query) -> Any:
        handler = self._handlers[type(query)]
        handler_instance = self._injector.get(handler)
        return handler_instance.handle(query)

    def register(self, query: type[Query], handler: type[QueryHandler]) -> None:
        self._handlers[query] = handler
