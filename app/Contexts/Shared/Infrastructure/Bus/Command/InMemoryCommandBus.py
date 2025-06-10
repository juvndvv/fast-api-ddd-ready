import logging

from injector import Injector, inject, singleton

from app.Contexts.Shared.Application.Bus.Command.Command import Command
from app.Contexts.Shared.Application.Bus.Command.CommandBus import CommandBus
from app.Contexts.Shared.Application.Bus.Command.CommandHandler import CommandHandler


@singleton
class InMemoryCommandBus(CommandBus):
    _logger: logging.Logger = logging.getLogger(__name__)

    @inject
    def __init__(self, injector: Injector) -> None:
        self._injector = injector
        self._handlers: dict[type[Command], type[CommandHandler]] = {}

    async def dispatch(self, command: Command) -> None:
        handler = self._handlers[type(command)]

        handler_instance = self._injector.get(handler)
        await handler_instance.handle(command)

    def register(self, command: type[Command], handler: type[CommandHandler]) -> None:
        self._handlers[command] = handler
