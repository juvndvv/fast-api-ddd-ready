from abc import ABC, abstractmethod

from app.Contexts.Shared.Application.Bus.Command.Command import Command
from app.Contexts.Shared.Application.Bus.Command.CommandHandler import CommandHandler


class CommandBus(ABC):
    @abstractmethod
    async def dispatch(self, command: Command) -> None:
        pass

    @abstractmethod
    def register(self, command: type[Command], handler: type[CommandHandler]) -> None:
        pass
