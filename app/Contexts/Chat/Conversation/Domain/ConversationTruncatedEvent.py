from __future__ import annotations

from typing import Any

from app.Contexts.Shared.Domain.DomainEvent import DomainEvent


class ConversationTruncatedEvent(DomainEvent):
    """Evento de dominio que se publica cuando se trunca una conversación"""

    def __init__(self, conversation_id: str, from_message_id: str) -> None:
        payload: dict[str, Any] = {
            "conversation_id": conversation_id,
            "from_message_id": from_message_id,
        }
        super().__init__(payload)

    @classmethod
    def event_name(cls) -> str:
        return "conversation.truncated"
