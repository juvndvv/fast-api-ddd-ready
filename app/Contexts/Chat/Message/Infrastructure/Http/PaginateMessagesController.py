import json

from fastapi import APIRouter, Query, Response, status
from injector import inject

from app.Contexts.Chat.Message.Application.Search.PaginateMessagesQuery import (
    PaginateMessagesQuery,
)
from app.Contexts.Chat.Message.Application.Search.PaginateMessagesQueryHandler import (
    PaginateMessagesQueryHandler,
)
from app.Contexts.Shared.Infrastructure.Http.Controller import Controller


class PaginateMessagesController(Controller):
    """Controlador HTTP para paginar mensajes en conversaciones"""

    @inject
    def __init__(self, query_handler: PaginateMessagesQueryHandler) -> None:
        self._query_handler = query_handler

    async def paginate_messages(
        self,
        conversation_id: str,
        cursor: str | None = Query(default=None),
        limit: int | None = Query(default=None),
    ) -> Response:
        """
        GET /conversations/{conversation_id}/messages
        Implementa AC6: paginación de mensajes con cursor
        """
        try:
            # Crear query de paginación
            query = PaginateMessagesQuery(
                conversation_id=conversation_id,
                cursor=cursor,
                limit=limit,
            )

            # Ejecutar query
            result = await self._query_handler.handle(query)

            # Retornar respuesta con paginación
            response_body = json.dumps(result)
            return Response(
                content=response_body,
                status_code=status.HTTP_200_OK,
                media_type="application/json",
            )

        except Exception:
            # Error interno del servidor
            error_body = json.dumps({"error": "Internal server error"})
            return Response(
                content=error_body,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                media_type="application/json",
            )

    def get_router(self) -> APIRouter:
        """Obtiene el router de la API para este controlador"""
        router = APIRouter()
        router.add_api_route(
            "/conversations/{conversation_id}/messages",
            self.paginate_messages,
            methods=["GET"],
            status_code=status.HTTP_200_OK,
        )
        return router
