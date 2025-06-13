from unittest.mock import Mock

import pytest

from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId
from app.Contexts.Chat.Message.Application.Search.PaginateMessagesQuery import (
    PaginateMessagesQuery,
)
from app.Contexts.Chat.Message.Application.Search.PaginateMessagesQueryHandler import (
    PaginateMessagesQueryHandler,
)
from app.Contexts.Chat.Message.Domain.Message import Message
from app.Contexts.Chat.Message.Domain.MessageContent import MessageContent
from app.Contexts.Chat.Message.Domain.MessageId import MessageId
from app.Contexts.Chat.Message.Infrastructure.Repository.MessageRepository import (
    MessageRepository,
)


class TestPaginateMessagesQueryHandler:
    @pytest.fixture
    def mock_message_repo(self) -> Mock:
        return Mock(spec=MessageRepository)

    @pytest.fixture
    def handler(self, mock_message_repo: Mock) -> PaginateMessagesQueryHandler:
        return PaginateMessagesQueryHandler(mock_message_repo)

    @pytest.mark.unit
    async def test_paginates_messages_with_cursor(
        self, handler: PaginateMessagesQueryHandler, mock_message_repo: Mock
    ) -> None:
        """Test AC6: GET messages con cursor devuelve lote y next-cursor"""
        # Arrange
        query = PaginateMessagesQuery(
            conversation_id="conv-123", cursor="msg-100", limit=2
        )

        # Simular mensajes devueltos por el repositorio
        messages = [
            Message.create(
                MessageId("msg-101"),
                ConversationId("conv-123"),
                MessageContent("Mensaje 1"),
            ),
            Message.create(
                MessageId("msg-102"),
                ConversationId("conv-123"),
                MessageContent("Mensaje 2"),
            ),
        ]
        mock_message_repo.paginate_messages.return_value = messages

        # Act
        result = await handler.handle(query)

        # Assert
        assert result is not None
        assert "messages" in result
        assert "next_cursor" in result
        assert "has_more" in result

        assert len(result["messages"]) == 2
        assert result["messages"][0]["id"] == "msg-101"
        assert result["messages"][1]["id"] == "msg-102"
        assert result["next_cursor"] == "msg-102"  # Último mensaje como cursor
        assert result["has_more"]  # Asumimos que hay más si devolvió el límite completo

        mock_message_repo.paginate_messages.assert_called_once_with(
            ConversationId("conv-123"), "msg-100", 2
        )

    @pytest.mark.unit
    async def test_paginates_messages_without_cursor(
        self, handler: PaginateMessagesQueryHandler, mock_message_repo: Mock
    ) -> None:
        """Test paginación desde el inicio (sin cursor)"""
        # Arrange
        query = PaginateMessagesQuery(conversation_id="conv-123", cursor=None, limit=3)

        messages = [
            Message.create(
                MessageId("msg-001"),
                ConversationId("conv-123"),
                MessageContent("Primer mensaje"),
            ),
            Message.create(
                MessageId("msg-002"),
                ConversationId("conv-123"),
                MessageContent("Segundo mensaje"),
            ),
        ]
        mock_message_repo.paginate_messages.return_value = messages

        # Act
        result = await handler.handle(query)

        # Assert
        assert result["next_cursor"] == "msg-002"
        assert not result["has_more"]  # Menos mensajes que el límite = no hay más

        mock_message_repo.paginate_messages.assert_called_once_with(
            ConversationId("conv-123"), None, 3
        )

    @pytest.mark.unit
    async def test_respects_pagination_limit(
        self, handler: PaginateMessagesQueryHandler, mock_message_repo: Mock
    ) -> None:
        """Test que respeta el límite máximo de 100 mensajes por lote"""
        # Arrange
        query = PaginateMessagesQuery(
            conversation_id="conv-123",
            cursor=None,
            limit=150,  # Más del límite máximo
        )

        mock_message_repo.paginate_messages.return_value = []

        # Act
        await handler.handle(query)

        # Assert - Debe limitar a 100
        mock_message_repo.paginate_messages.assert_called_once_with(
            ConversationId("conv-123"), None, 100
        )

    @pytest.mark.unit
    async def test_handles_empty_result(
        self, handler: PaginateMessagesQueryHandler, mock_message_repo: Mock
    ) -> None:
        """Test manejo de resultado vacío"""
        # Arrange
        query = PaginateMessagesQuery(
            conversation_id="conv-123", cursor="msg-999", limit=10
        )

        mock_message_repo.paginate_messages.return_value = []

        # Act
        result = await handler.handle(query)

        # Assert
        assert result["messages"] == []
        assert result["next_cursor"] is None
        assert not result["has_more"]
