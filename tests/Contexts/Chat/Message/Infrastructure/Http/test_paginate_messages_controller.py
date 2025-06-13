from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import status

from app.Contexts.Chat.Message.Application.Search.PaginateMessagesQuery import (
    PaginateMessagesQuery,
)
from app.Contexts.Chat.Message.Application.Search.PaginateMessagesQueryHandler import (
    PaginateMessagesQueryHandler,
)
from app.Contexts.Chat.Message.Infrastructure.Http.PaginateMessagesController import (
    PaginateMessagesController,
)


class TestPaginateMessagesController:
    @pytest.fixture
    def mock_query_handler(self) -> Mock:
        mock = Mock(spec=PaginateMessagesQueryHandler)
        mock.handle = AsyncMock()
        return mock

    @pytest.fixture
    def controller(self, mock_query_handler: Mock) -> PaginateMessagesController:
        return PaginateMessagesController(mock_query_handler)

    @pytest.mark.unit
    async def test_paginate_messages_returns_paginated_messages(
        self, controller: PaginateMessagesController, mock_query_handler: Mock
    ) -> None:
        """Test AC6: GET messages with pagination"""
        # Arrange
        conversation_id = "conv-123"
        mock_query_handler.handle.return_value = {
            "messages": [
                {
                    "id": "msg-1",
                    "content": "Message 1",
                    "conversation_id": "conv-123",
                }
            ],
            "has_more": False,
            "next_cursor": None,
        }

        # Act
        response = await controller.paginate_messages(
            conversation_id=conversation_id, cursor=None, limit=10
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK

        # Verify handler was called with correct query
        mock_query_handler.handle.assert_called_once()
        query_arg = mock_query_handler.handle.call_args[0][0]
        assert isinstance(query_arg, PaginateMessagesQuery)
        assert query_arg.conversation_id == conversation_id
        assert query_arg.cursor is None
        assert query_arg.limit == 10

    @pytest.mark.unit
    async def test_paginate_messages_with_cursor_and_limit(
        self, controller: PaginateMessagesController, mock_query_handler: Mock
    ) -> None:
        """Test pagination with cursor and custom limit"""
        # Arrange
        conversation_id = "conv-123"
        cursor = "msg-5"
        limit = 20

        mock_query_handler.handle.return_value = {
            "messages": [],
            "has_more": False,
            "next_cursor": None,
        }

        # Act
        response = await controller.paginate_messages(
            conversation_id=conversation_id, cursor=cursor, limit=limit
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK

        # Verify correct parameters passed
        query_arg = mock_query_handler.handle.call_args[0][0]
        assert query_arg.cursor == cursor
        assert query_arg.limit == limit

    @pytest.mark.unit
    async def test_paginate_messages_uses_default_limit_when_none(
        self, controller: PaginateMessagesController, mock_query_handler: Mock
    ) -> None:
        """Test that default limit is used when none provided"""
        # Arrange
        conversation_id = "conv-123"
        mock_query_handler.handle.return_value = {
            "messages": [],
            "has_more": False,
            "next_cursor": None,
        }

        # Act
        response = await controller.paginate_messages(
            conversation_id=conversation_id, cursor=None, limit=None
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK

        # Verify default limit of 20 is used
        query_arg = mock_query_handler.handle.call_args[0][0]
        assert query_arg.limit == 20

    @pytest.mark.unit
    async def test_paginate_messages_handles_query_handler_error(
        self, controller: PaginateMessagesController, mock_query_handler: Mock
    ) -> None:
        """Test error handling when query handler fails"""
        # Arrange
        conversation_id = "conv-123"
        mock_query_handler.handle.side_effect = RuntimeError("Database error")

        # Act
        response = await controller.paginate_messages(
            conversation_id=conversation_id, cursor=None, limit=10
        )

        # Assert
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert b"Internal server error" in response.body
