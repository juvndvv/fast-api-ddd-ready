import logging

from injector import Binder, Module

from app.Contexts.Shared.Application.Bus.Command.Command import Command
from app.Contexts.Shared.Application.Bus.Command.CommandBus import CommandBus
from app.Contexts.Shared.Application.Bus.Command.CommandHandler import CommandHandler
from app.Contexts.Shared.Application.Bus.Event.EventListener import EventListener
from app.Contexts.Shared.Application.Bus.Query.Query import Query
from app.Contexts.Shared.Application.Bus.Query.QueryBus import QueryBus
from app.Contexts.Shared.Application.Bus.Query.QueryHandler import QueryHandler
from app.Contexts.Shared.Domain.DomainEvent import DomainEvent
from app.Contexts.Shared.Domain.ExceptionHandling.ExceptionHandler import (
    ExceptionHandler,
)
from app.Contexts.Shared.Infrastructure.Bus.Command.InMemoryCommandBus import (
    InMemoryCommandBus,
)
from app.Contexts.Shared.Infrastructure.Bus.Query.InMemoryQueryBus import (
    InMemoryQueryBus,
)
from app.Contexts.Shared.Infrastructure.ExceptionHandling.SentryExceptionHandler import (
    SentryExceptionHandler,
)


class ApplicationModule(Module):
    _logger: logging.Logger = logging.getLogger(__name__)

    def configure(self, binder: Binder) -> None:
        self._logger.info("Configuring application module")

        binder.bind(CommandBus, to=InMemoryCommandBus)  # type: ignore
        binder.bind(QueryBus, to=InMemoryQueryBus)  # type: ignore
        binder.bind(ExceptionHandler, to=SentryExceptionHandler)  # type: ignore

    def map_commands(self) -> list[tuple[type[Command], type[CommandHandler]]]:
        return []

    def map_queries(self) -> list[tuple[type[Query], type[QueryHandler]]]:
        return []

    def map_events(self) -> list[tuple[type[DomainEvent], type[EventListener]]]:
        return []
