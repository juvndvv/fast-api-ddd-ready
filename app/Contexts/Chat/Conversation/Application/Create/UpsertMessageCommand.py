from app.Contexts.Shared.Application.Bus.Command.Command import Command


class UpsertMessageCommand(Command):
    """Comando para crear o actualizar un mensaje en una conversación"""

    def __init__(
        self, conversation_id: str, message_id: str, content: str, owner: str
    ) -> None:
        self.conversation_id = conversation_id
        self.message_id = message_id
        self.content = content
        self.owner = owner
