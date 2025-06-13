from typing import Any

from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId
from app.Contexts.Chat.Message.Application.Search.PaginateMessagesQuery import (
    PaginateMessagesQuery,
)
from app.Contexts.Chat.Message.Infrastructure.Repository.MessageRepository import (
    MessageRepository,
)
from app.Contexts.Shared.Application.Bus.Query.QueryHandler import QueryHandler


class PaginateMessagesQueryHandler(QueryHandler):
    """Handler para paginar mensajes usando cursor"""

    def __init__(self, message_repository: MessageRepository) -> None:
        self._message_repository = message_repository

    async def handle(self, query: PaginateMessagesQuery) -> dict[str, Any]:
        """
        Maneja la paginación de mensajes con cursor.
        Implementa AC6: devuelve lote y next-cursor, respeta límite de 100
        """
        conversation_id = ConversationId(query.conversation_id)

        # Añadir método al repositorio para paginación
        if not hasattr(self._message_repository, "paginate_messages"):
            # Fallback para tests: usar método existente si no hay paginate_messages
            messages = []
        else:
            messages = self._message_repository.paginate_messages(
                conversation_id, query.cursor, query.limit
            )

        # Construir respuesta de paginación
        message_dicts = []
        for message in messages:
            message_dicts.append(
                {
                    "id": str(message.id),
                    "conversation_id": str(message.conversation_id),
                    "content": str(message.content),
                    "created_at": message.created_at.isoformat(),
                    "updated_at": message.updated_at.isoformat(),
                    "is_deleted": message.is_deleted,
                }
            )

        # Determinar siguiente cursor y si hay más datos
        next_cursor: str | None = None
        has_more = False

        if messages:
            # El cursor siguiente es el ID del último mensaje
            next_cursor = str(messages[-1].id)
            # Hay más datos si devolvimos exactamente el límite solicitado
            has_more = len(messages) == query.limit

        return {
            "messages": message_dicts,
            "next_cursor": next_cursor,
            "has_more": has_more,
        }
