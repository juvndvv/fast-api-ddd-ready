from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import status

from app.Contexts.Chat.Conversation.Application.Search.GetConversationQuery import (
    GetConversationQuery,
)
from app.Contexts.Chat.Conversation.Application.Search.GetConversationQueryHandler import (
    GetConversationQueryHandler,
)
from app.Contexts.Chat.Conversation.Infrastructure.Http.GetConversationController import (
    GetConversationController,
)


class TestGetConversationController:
    @pytest.fixture
    def mock_query_handler(self) -> Mock:
        mock = Mock(spec=GetConversationQueryHandler)
        mock.handle = AsyncMock()
        return mock

    @pytest.fixture
    def controller(self, mock_query_handler: Mock) -> GetConversationController:
        return GetConversationController(mock_query_handler)

    @pytest.mark.unit
    async def test_get_conversation_returns_conversation_data(
        self, controller: GetConversationController, mock_query_handler: Mock
    ) -> None:
        """Test que devuelve datos de conversación existente"""
        # Arrange
        conversation_id = "conv-123"
        conversation_data = {
            "id": "conv-123",
            "owner": "user-456",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
            "last_message_id": "msg-789",
        }
        mock_query_handler.handle.return_value = conversation_data

        # Act
        response = await controller.get_conversation(conversation_id)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.body is not None

        # Verificar que se llamó al handler con el query correcto
        mock_query_handler.handle.assert_called_once()
        query_arg = mock_query_handler.handle.call_args[0][0]
        assert isinstance(query_arg, GetConversationQuery)
        assert query_arg.conversation_id == conversation_id

    @pytest.mark.unit
    async def test_get_conversation_returns_not_found_when_conversation_doesnt_exist(
        self, controller: GetConversationController, mock_query_handler: Mock
    ) -> None:
        """Test que devuelve 404 cuando la conversación no existe"""
        # Arrange
        conversation_id = "conv-nonexistent"
        mock_query_handler.handle.return_value = None

        # Act
        response = await controller.get_conversation(conversation_id)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

        mock_query_handler.handle.assert_called_once()
        query_arg = mock_query_handler.handle.call_args[0][0]
        assert query_arg.conversation_id == conversation_id
