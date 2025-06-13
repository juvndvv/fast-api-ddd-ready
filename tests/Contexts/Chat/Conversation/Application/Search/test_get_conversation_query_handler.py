from unittest.mock import Mock

import pytest

from app.Contexts.Chat.Conversation.Application.Search.GetConversationQuery import (
    GetConversationQuery,
)
from app.Contexts.Chat.Conversation.Application.Search.GetConversationQueryHandler import (
    GetConversationQueryHandler,
)
from app.Contexts.Chat.Conversation.Domain.Conversation import Conversation
from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId
from app.Contexts.Chat.Conversation.Domain.ConversationOwner import ConversationOwner
from app.Contexts.Chat.Conversation.Infrastructure.Repository.ConversationRepository import (
    ConversationRepository,
)
from app.Contexts.Chat.Message.Infrastructure.Repository.MessageRepository import (
    MessageRepository,
)


class TestGetConversationQueryHandler:
    @pytest.fixture
    def mock_conversation_repo(self) -> Mock:
        return Mock(spec=ConversationRepository)

    @pytest.fixture
    def mock_message_repo(self) -> Mock:
        return Mock(spec=MessageRepository)

    @pytest.fixture
    def handler(
        self, mock_conversation_repo: Mock, mock_message_repo: Mock
    ) -> GetConversationQueryHandler:
        return GetConversationQueryHandler(mock_conversation_repo, mock_message_repo)

    @pytest.mark.unit
    async def test_gets_conversation_without_messages(
        self,
        handler: GetConversationQueryHandler,
        mock_conversation_repo: Mock,
        mock_message_repo: Mock,
    ) -> None:
        """Test AC5: GET conversation NO debe ejecutar consulta de mensajes"""
        # Arrange
        query = GetConversationQuery(conversation_id="conv-123")

        existing_conversation = Conversation.create(
            ConversationId("conv-123"), ConversationOwner("user-456")
        )
        mock_conversation_repo.find_by_id.return_value = existing_conversation

        # Act
        result = await handler.handle(query)

        # Assert
        assert result is not None
        assert result["id"] == "conv-123"
        assert result["owner"] == "user-456"
        assert "created_at" in result
        assert "updated_at" in result

        # CRITICAL: Verificar que NO se llamó al repositorio de mensajes
        mock_message_repo.assert_not_called()
        mock_conversation_repo.find_by_id.assert_called_once_with(
            ConversationId("conv-123")
        )

    @pytest.mark.unit
    async def test_returns_none_when_conversation_not_found(
        self,
        handler: GetConversationQueryHandler,
        mock_conversation_repo: Mock,
        mock_message_repo: Mock,
    ) -> None:
        """Test que retorna None cuando la conversación no existe"""
        # Arrange
        query = GetConversationQuery(conversation_id="conv-nonexistent")
        mock_conversation_repo.find_by_id.return_value = None

        # Act
        result = await handler.handle(query)

        # Assert
        assert result is None
        mock_message_repo.assert_not_called()
        mock_conversation_repo.find_by_id.assert_called_once_with(
            ConversationId("conv-nonexistent")
        )
