from abc import ABC, abstractmethod

from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId
from app.Contexts.Chat.Message.Domain.Message import Message
from app.Contexts.Chat.Message.Domain.MessageId import MessageId


class MessageRepository(ABC):
    """Interfaz del repositorio de mensajes"""

    @abstractmethod
    def find_by_id(self, message_id: MessageId) -> Message | None:
        """Busca un mensaje por su ID"""
        pass

    @abstractmethod
    def save(self, message: Message) -> None:
        """Guarda un mensaje"""
        pass

    @abstractmethod
    def find_messages_after(
        self, conversation_id: ConversationId, message_id: MessageId
    ) -> list[MessageId]:
        """Encuentra los IDs de mensajes posteriores a uno dado en una conversación"""
        pass

    @abstractmethod
    def soft_delete_messages(self, message_ids: list[MessageId]) -> None:
        """Marca como eliminados (soft delete) una lista de mensajes"""
        pass
