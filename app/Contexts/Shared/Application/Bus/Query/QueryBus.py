from abc import ABC, abstractmethod
from typing import Any

from app.Contexts.Shared.Application.Bus.Query.Query import Query
from app.Contexts.Shared.Application.Bus.Query.QueryHandler import QueryHandler


class QueryBus(ABC):
    @abstractmethod
    def ask(self, query: Query) -> Any:
        pass

    @abstractmethod
    def register(self, query: type[Query], handler: type[QueryHandler]) -> None:
        pass
