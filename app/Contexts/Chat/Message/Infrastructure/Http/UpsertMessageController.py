import json
from typing import Any

from fastapi import APIRouter, Response, status
from injector import inject

from app.Contexts.Chat.Message.Application.Create.UpsertMessageCommand import (
    UpsertMessageCommand,
)
from app.Contexts.Chat.Message.Application.Create.UpsertMessageCommandHandler import (
    UpsertMessageCommandHandler,
)
from app.Contexts.Shared.Infrastructure.Http.Controller import Controller


class UpsertMessageController(Controller):
    """Controlador HTTP para crear/actualizar mensajes en conversaciones"""

    @inject
    def __init__(self, command_handler: UpsertMessageCommandHandler) -> None:
        self._command_handler = command_handler

    async def upsert_message(
        self, conversation_id: str, message_id: str, request_body: dict[str, Any]
    ) -> Response:
        """
        PUT /conversation/{conversation_id}/message/{message_id}
        Implementa AC1-4: creación/actualización con validaciones
        """
        try:
            # AC4: Validar consistencia de IDs path vs body
            body_message_id = request_body.get("id")
            if body_message_id != message_id:
                raise ValueError("Message ID en path y body deben coincidir")

            # Extraer datos del body
            content = request_body.get("content", "")
            owner = request_body.get("owner", "")

            # AC3: Validación temprana (será validada de nuevo en domain)
            if not content.strip():
                raise ValueError("MessageContent no puede estar vacío")

            if not owner.strip():
                raise ValueError("Owner no puede estar vacío")

            # Crear y ejecutar comando
            command = UpsertMessageCommand(
                conversation_id=conversation_id,
                message_id=message_id,
                content=content,
                owner=owner,
            )

            await self._command_handler.handle(command)

            # AC1 & AC8: Respuesta exitosa (idempotente)
            response_body = json.dumps({"message": "Message upserted successfully"})
            return Response(
                content=response_body,
                status_code=status.HTTP_201_CREATED,
                media_type="application/json",
            )

        except ValueError as e:
            # AC3 & AC4: Retornar error 400 para validaciones
            error_body = json.dumps({"error": str(e)})
            return Response(
                content=error_body,
                status_code=status.HTTP_400_BAD_REQUEST,
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
            "/conversations/{conversation_id}/messages/{message_id}",
            self.upsert_message,
            methods=["PUT"],
            status_code=status.HTTP_201_CREATED,
        )
        return router
