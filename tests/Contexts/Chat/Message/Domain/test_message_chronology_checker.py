from unittest.mock import Mock

import pytest

from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId
from app.Contexts.Chat.Message.Domain.MessageChronologyChecker import (
    MessageChronologyChecker,
)
from app.Contexts.Chat.Message.Domain.MessageId import MessageId
from app.Contexts.Chat.Message.Infrastructure.Repository.MessageRepository import (
    MessageRepository,
)


class TestMessageChronologyChecker:
    @pytest.mark.unit
    def test_validates_message_can_be_inserted(self) -> None:
        """Test que valida que un mensaje puede ser insertado en una posición válida"""
        mock_repo = Mock(spec=MessageRepository)
        mock_repo.find_messages_after.return_value = []

        checker = MessageChronologyChecker(mock_repo)
        conversation_id = ConversationId("conv-123")
        message_id = MessageId("msg-456")

        # No hay mensajes posteriores, se puede insertar
        result = checker.can_insert_message(conversation_id, message_id)

        assert result is True
        mock_repo.find_messages_after.assert_called_once_with(
            conversation_id, message_id
        )

    @pytest.mark.unit
    def test_validates_message_cannot_be_inserted_with_posterior_messages(self) -> None:
        """Test que valida que un mensaje no se puede insertar si hay mensajes posteriores"""
        mock_repo = Mock(spec=MessageRepository)
        mock_repo.find_messages_after.return_value = [MessageId("msg-789")]

        checker = MessageChronologyChecker(mock_repo)
        conversation_id = ConversationId("conv-123")
        message_id = MessageId("msg-456")

        # Hay mensajes posteriores, no se puede insertar
        result = checker.can_insert_message(conversation_id, message_id)

        assert result is False
        mock_repo.find_messages_after.assert_called_once_with(
            conversation_id, message_id
        )

    @pytest.mark.unit
    def test_gets_messages_after(self) -> None:
        """Test que obtiene los mensajes posteriores a uno dado"""
        mock_repo = Mock(spec=MessageRepository)
        expected_messages = [MessageId("msg-789"), MessageId("msg-012")]
        mock_repo.find_messages_after.return_value = expected_messages

        checker = MessageChronologyChecker(mock_repo)
        conversation_id = ConversationId("conv-123")
        message_id = MessageId("msg-456")

        result = checker.get_messages_after(conversation_id, message_id)

        assert result == expected_messages
        mock_repo.find_messages_after.assert_called_once_with(
            conversation_id, message_id
        )
