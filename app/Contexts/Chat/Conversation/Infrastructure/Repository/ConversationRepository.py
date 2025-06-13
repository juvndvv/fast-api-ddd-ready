from abc import ABC, abstractmethod

from app.Contexts.Chat.Conversation.Domain.Conversation import Conversation
from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId


class ConversationRepository(ABC):
    """Interfaz del repositorio de conversaciones"""

    @abstractmethod
    def find_by_id(self, conversation_id: ConversationId) -> Conversation | None:
        """Busca una conversación por su ID"""
        pass

    @abstractmethod
    def save(self, conversation: Conversation) -> None:
        """Guarda una conversación"""
        pass
