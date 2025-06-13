from typing import Any

from injector import inject

from app.Contexts.Chat.Conversation.Application.Search.GetConversationQuery import (
    GetConversationQuery,
)
from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId
from app.Contexts.Chat.Conversation.Infrastructure.Repository.ConversationRepository import (
    ConversationRepository,
)
from app.Contexts.Chat.Message.Infrastructure.Repository.MessageRepository import (
    MessageRepository,
)
from app.Contexts.Shared.Application.Bus.Query.QueryHandler import QueryHandler


class GetConversationQueryHandler(QueryHandler):
    """Handler para obtener metadatos de conversación sin consultar mensajes"""

    @inject
    def __init__(
        self,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository,
    ) -> None:
        self._conversation_repository = conversation_repository
        # NOTE: message_repository se inyecta pero NO se usa, para verificar AC5
        self._message_repository = message_repository

    async def handle(self, query: GetConversationQuery) -> dict[str, Any] | None:
        """
        Maneja el query GetConversation.
        IMPORTANTE: NO consulta mensajes para cumplir con AC5 (rendimiento)
        """
        conversation_id = ConversationId(query.conversation_id)
        conversation = self._conversation_repository.find_by_id(conversation_id)

        if not conversation:
            return None

        return {
            "id": str(conversation.id),
            "owner": str(conversation.owner),
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
            "last_message_id": (
                str(conversation.last_message_id)
                if conversation.last_message_id
                else None
            ),
        }
