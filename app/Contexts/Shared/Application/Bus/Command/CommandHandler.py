from abc import ABC, abstractmethod

from app.Contexts.Shared.Application.Bus.Command.Command import Command


class CommandHandler(ABC):
    @abstractmethod
    def handle(self, command: Command) -> None:
        pass
