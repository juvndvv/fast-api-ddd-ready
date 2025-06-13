from __future__ import annotations

from typing import Any

from app.Contexts.Shared.Domain.DomainEvent import DomainEvent


class ConversationCreatedEvent(DomainEvent):
    """Evento de dominio que se publica cuando se crea una conversación"""

    def __init__(self, conversation_id: str, owner: str) -> None:
        payload: dict[str, Any] = {
            "conversation_id": conversation_id,
            "owner": owner,
        }
        super().__init__(payload)

    @classmethod
    def event_name(cls) -> str:
        return "conversation.created"
