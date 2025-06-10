from abc import ABC, abstractmethod

from app.Contexts.Shared.Application.Bus.Event.EventListener import EventListener
from app.Contexts.Shared.Domain.DomainEvent import DomainEvent


class EventBus(ABC):
    @abstractmethod
    async def publish(self, events: list[DomainEvent]) -> None:
        """Publica una lista de eventos de dominio"""
        pass

    @abstractmethod
    def register(self, event: type[DomainEvent], listener: type[EventListener]) -> None:
        """Registra un listener para un tipo de evento específico"""
        pass

    @abstractmethod
    def subscribe(self, event: type[DomainEvent], listener: EventListener) -> None:
        pass
