"""
In-memory implementation of ConversationRepository for testing.
"""

from app.Contexts.Chat.Conversation.Domain.Conversation import Conversation
from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId
from app.Contexts.Chat.Conversation.Infrastructure.Repository.ConversationRepository import (
    ConversationRepository,
)


class InMemoryConversationRepository(ConversationRepository):
    """In-memory implementation of ConversationRepository for testing"""

    def __init__(self) -> None:
        self._conversations: dict[str, Conversation] = {}

    def find_by_id(self, conversation_id: ConversationId) -> Conversation | None:
        """Busca una conversación por su ID"""
        return self._conversations.get(str(conversation_id))

    def save(self, conversation: Conversation) -> None:
        """Guarda una conversación"""
        self._conversations[str(conversation.id)] = conversation
