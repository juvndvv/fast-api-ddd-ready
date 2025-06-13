"""
In-memory implementation of MessageRepository for testing.
"""

from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId
from app.Contexts.Chat.Message.Domain.Message import Message
from app.Contexts.Chat.Message.Domain.MessageId import MessageId
from app.Contexts.Chat.Message.Infrastructure.Repository.MessageRepository import (
    MessageRepository,
)


class InMemoryMessageRepository(MessageRepository):
    """In-memory implementation of MessageRepository for testing"""

    def __init__(self) -> None:
        self._messages: dict[str, Message] = {}

    def find_by_id(self, message_id: MessageId) -> Message | None:
        """Busca un mensaje por su ID"""
        return self._messages.get(str(message_id))

    def save(self, message: Message) -> None:
        """Guarda un mensaje"""
        self._messages[str(message.id)] = message

    def find_messages_after(
        self, conversation_id: ConversationId, message_id: MessageId
    ) -> list[MessageId]:
        """Encuentra mensajes posteriores a uno dado en una conversación"""
        # Implementación simple: retorna lista vacía
        # En implementación real buscaría por timestamp/orden
        return []

    def soft_delete_messages(self, message_ids: list[MessageId]) -> None:
        """Soft delete de una lista de mensajes"""
        for message_id in message_ids:
            message = self._messages.get(str(message_id))
            if message:
                message.soft_delete()

    def paginate_messages(
        self, conversation_id: ConversationId, cursor: str | None, limit: int
    ) -> list[Message]:
        """Pagina mensajes de una conversación usando cursor"""
        # Implementación simple: retorna mensajes de la conversación
        conversation_messages = [
            msg
            for msg in self._messages.values()
            if str(msg.conversation_id) == str(conversation_id) and not msg.is_deleted
        ]
        # Aplicar límite
        return conversation_messages[:limit]
