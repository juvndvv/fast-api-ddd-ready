from abc import ABC, abstractmethod

from app.Contexts.Shared.Application.Bus.Query.Query import Query


class QueryHandler(ABC):
    @abstractmethod
    def handle(self, query: Query) -> None:
        pass
