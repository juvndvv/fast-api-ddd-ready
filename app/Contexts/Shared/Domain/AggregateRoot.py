from app.Contexts.Shared.Domain.DomainEvent import DomainEvent


class AggregateRoot:
    def __init__(self) -> None:
        self._events: list[DomainEvent] = []

    def pull_domain_events(self) -> list[DomainEvent]:
        """Obtiene y limpia los eventos de dominio pendientes"""
        events = self._events.copy()
        self._events.clear()
        return events

    def _record(self, event: DomainEvent) -> None:
        """Registra un evento de dominio"""
        self._events.append(event)

    def has_events(self) -> bool:
        """Verifica si el agregado tiene eventos pendientes"""
        return len(self._events) > 0
