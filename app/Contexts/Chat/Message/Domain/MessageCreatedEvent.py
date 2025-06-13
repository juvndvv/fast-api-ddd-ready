from __future__ import annotations

from typing import Any

from app.Contexts.Shared.Domain.DomainEvent import DomainEvent


class MessageCreatedEvent(DomainEvent):
    """Evento de dominio que se publica cuando se crea un mensaje"""

    def __init__(self, message_id: str, conversation_id: str, content: str) -> None:
        payload: dict[str, Any] = {
            "message_id": message_id,
            "conversation_id": conversation_id,
            "content": content,
        }
        super().__init__(payload)

    @classmethod
    def event_name(cls) -> str:
        return "message.created"
