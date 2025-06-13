from __future__ import annotations

from datetime import UTC, datetime

from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId
from app.Contexts.Chat.Message.Domain.MessageContent import MessageContent
from app.Contexts.Chat.Message.Domain.MessageCreatedEvent import MessageCreatedEvent
from app.Contexts.Chat.Message.Domain.MessageId import MessageId
from app.Contexts.Chat.Message.Domain.MessageUpdatedEvent import MessageUpdatedEvent
from app.Contexts.Shared.Domain.AggregateRoot import AggregateRoot
from app.Contexts.Shared.Domain.DomainEvent import DomainEvent


class Message(AggregateRoot):
    """Aggregate root para mensajes"""

    def __init__(
        self,
        id: MessageId,
        conversation_id: ConversationId,
        content: MessageContent,
        created_at: datetime,
        updated_at: datetime,
        is_deleted: bool = False,
    ) -> None:
        super().__init__()
        self._id = id
        self._conversation_id = conversation_id
        self._content = content
        self._created_at = created_at
        self._updated_at = updated_at
        self._is_deleted = is_deleted

    @classmethod
    def create(
        cls, id: MessageId, conversation_id: ConversationId, content: MessageContent
    ) -> Message:
        """Factory method para crear un nuevo mensaje"""
        now = datetime.now(UTC)
        message = cls(
            id=id,
            conversation_id=conversation_id,
            content=content,
            created_at=now,
            updated_at=now,
        )
        message._record(
            MessageCreatedEvent(str(id), str(conversation_id), str(content))
        )
        return message

    @property
    def id(self) -> MessageId:
        return self._id

    @property
    def conversation_id(self) -> ConversationId:
        return self._conversation_id

    @property
    def content(self) -> MessageContent:
        return self._content

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def is_deleted(self) -> bool:
        return self._is_deleted

    def update_content(self, new_content: MessageContent) -> None:
        """Actualiza el contenido del mensaje"""
        self._content = new_content
        self._updated_at = datetime.now(UTC)
        self._record(
            MessageUpdatedEvent(
                str(self._id), str(self._conversation_id), str(new_content)
            )
        )

    def soft_delete(self) -> None:
        """Marca el mensaje como eliminado (soft delete)"""
        self._is_deleted = True
        self._updated_at = datetime.now(UTC)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Message) and self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    @property
    def domain_events(self) -> list[DomainEvent]:
        """Compatibilidad con los tests existentes"""
        return self._events

    def clear_domain_events(self) -> None:
        """Limpia los eventos de dominio para compatibilidad con tests"""
        self._events.clear()
