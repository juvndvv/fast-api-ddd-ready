from abc import ABC, abstractmethod

from app.Contexts.Shared.Domain.DomainEvent import DomainEvent


class EventListener(ABC):
    @abstractmethod
    async def listen(self, event: DomainEvent) -> None:
        pass
