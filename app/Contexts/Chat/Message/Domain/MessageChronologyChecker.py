from injector import inject

from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId
from app.Contexts.Chat.Message.Domain.MessageId import MessageId
from app.Contexts.Chat.Message.Infrastructure.Repository.MessageRepository import (
    MessageRepository,
)


class MessageChronologyChecker:
    """Servicio de dominio para verificar cronología de mensajes"""

    @inject
    def __init__(self, message_repository: MessageRepository) -> None:
        self._message_repository = message_repository

    def can_insert_message(
        self, conversation_id: ConversationId, message_id: MessageId
    ) -> bool:
        """Verifica si un mensaje puede ser insertado en una conversación sin violar la cronología"""
        posterior_messages = self._message_repository.find_messages_after(
            conversation_id, message_id
        )
        return len(posterior_messages) == 0

    def get_messages_after(
        self, conversation_id: ConversationId, message_id: MessageId
    ) -> list[MessageId]:
        """Obtiene los mensajes posteriores a uno dado en una conversación"""
        return self._message_repository.find_messages_after(conversation_id, message_id)
