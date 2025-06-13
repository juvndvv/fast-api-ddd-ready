import json

from fastapi import APIRouter, Response, status
from injector import inject

from app.Contexts.Chat.Conversation.Application.Search.GetConversationQuery import (
    GetConversationQuery,
)
from app.Contexts.Chat.Conversation.Application.Search.GetConversationQueryHandler import (
    GetConversationQueryHandler,
)
from app.Contexts.Shared.Infrastructure.Http.Controller import Controller


class GetConversationController(Controller):
    """Controlador HTTP para obtener metadatos de conversación"""

    @inject
    def __init__(self, query_handler: GetConversationQueryHandler) -> None:
        self._query_handler = query_handler

    async def get_conversation(self, conversation_id: str) -> Response:
        """
        GET /conversation/{conversation_id}
        Implementa AC5: devuelve metadatos sin consultar mensajes
        """
        try:
            query = GetConversationQuery(conversation_id)
            result = await self._query_handler.handle(query)

            if result is None:
                # Conversación no encontrada
                return Response(
                    content=json.dumps({"error": "Conversation not found"}),
                    status_code=status.HTTP_404_NOT_FOUND,
                    media_type="application/json",
                )

            # Conversación encontrada
            response_body = json.dumps(result)
            return Response(
                content=response_body,
                status_code=status.HTTP_200_OK,
                media_type="application/json",
            )

        except Exception as e:
            # Log error y re-raise
            raise e

    def get_router(self) -> APIRouter:
        """Obtiene el router de la API para este controlador"""
        router = APIRouter()
        router.add_api_route(
            "/conversations/{conversation_id}",
            self.get_conversation,
            methods=["GET"],
            status_code=status.HTTP_200_OK,
        )
        return router
