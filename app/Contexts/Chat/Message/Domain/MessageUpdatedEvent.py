from __future__ import annotations

from typing import Any

from app.Contexts.Shared.Domain.DomainEvent import DomainEvent


class MessageUpdatedEvent(DomainEvent):
    """Evento de dominio que se publica cuando se actualiza un mensaje"""

    def __init__(self, message_id: str, conversation_id: str, new_content: str) -> None:
        payload: dict[str, Any] = {
            "message_id": message_id,
            "conversation_id": conversation_id,
            "new_content": new_content,
        }
        super().__init__(payload)

    @classmethod
    def event_name(cls) -> str:
        return "message.updated"
