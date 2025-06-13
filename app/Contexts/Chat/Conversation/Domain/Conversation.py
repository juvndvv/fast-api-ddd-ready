from __future__ import annotations

from datetime import UTC, datetime

from app.Contexts.Chat.Conversation.Domain.ConversationCreatedEvent import (
    ConversationCreatedEvent,
)
from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId
from app.Contexts.Chat.Conversation.Domain.ConversationOwner import ConversationOwner
from app.Contexts.Chat.Message.Domain.MessageId import MessageId
from app.Contexts.Shared.Domain.AggregateRoot import AggregateRoot
from app.Contexts.Shared.Domain.DomainEvent import DomainEvent


class Conversation(AggregateRoot):
    """Aggregate root para conversaciones"""

    def __init__(
        self,
        id: ConversationId,
        owner: ConversationOwner,
        created_at: datetime,
        updated_at: datetime,
        last_message_id: MessageId | None = None,
    ) -> None:
        super().__init__()
        self._id = id
        self._owner = owner
        self._created_at = created_at
        self._updated_at = updated_at
        self._last_message_id = last_message_id

    @classmethod
    def create(cls, id: ConversationId, owner: ConversationOwner) -> Conversation:
        """Factory method para crear una nueva conversación"""
        now = datetime.now(UTC)
        conversation = cls(
            id=id,
            owner=owner,
            created_at=now,
            updated_at=now,
        )
        conversation._record(ConversationCreatedEvent(str(id), str(owner)))
        return conversation

    @property
    def id(self) -> ConversationId:
        return self._id

    @property
    def owner(self) -> ConversationOwner:
        return self._owner

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def last_message_id(self) -> MessageId | None:
        return self._last_message_id

    def update_last_message(self, message_id: MessageId) -> None:
        """Actualiza el último mensaje de la conversación"""
        self._last_message_id = message_id
        self._updated_at = datetime.now(UTC)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Conversation) and self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    @property
    def domain_events(self) -> list[DomainEvent]:
        """Compatibilidad con los tests existentes"""
        return self._events
