from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import status

from app.Contexts.Chat.Message.Application.Create.UpsertMessageCommand import (
    UpsertMessageCommand,
)
from app.Contexts.Chat.Message.Application.Create.UpsertMessageCommandHandler import (
    UpsertMessageCommandHandler,
)
from app.Contexts.Chat.Message.Infrastructure.Http.UpsertMessageController import (
    UpsertMessageController,
)


class TestUpsertMessageController:
    @pytest.fixture
    def mock_command_handler(self) -> Mock:
        mock = Mock(spec=UpsertMessageCommandHandler)
        mock.handle = AsyncMock()
        return mock

    @pytest.fixture
    def controller(self, mock_command_handler: Mock) -> UpsertMessageController:
        return UpsertMessageController(mock_command_handler)

    @pytest.mark.unit
    async def test_upsert_message_creates_new_conversation_and_message(
        self, controller: UpsertMessageController, mock_command_handler: Mock
    ) -> None:
        """Test AC1: PUT sobre nueva conv.: conversación y mensaje creados, 201"""
        # Arrange
        conversation_id = "conv-123"
        message_id = "msg-456"
        request_body = {"id": message_id, "content": "Hola mundo", "owner": "user-789"}

        # Act
        response = await controller.upsert_message(
            conversation_id, message_id, request_body
        )

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.body == b'{"message": "Message upserted successfully"}'

        # Verificar que se llamó al handler con el comando correcto
        mock_command_handler.handle.assert_called_once()
        command_arg = mock_command_handler.handle.call_args[0][0]
        assert isinstance(command_arg, UpsertMessageCommand)
        assert command_arg.conversation_id == conversation_id
        assert command_arg.message_id == message_id
        assert command_arg.content == "Hola mundo"
        assert command_arg.owner == "user-789"

    @pytest.mark.unit
    async def test_upsert_message_updates_existing_message(
        self, controller: UpsertMessageController, mock_command_handler: Mock
    ) -> None:
        """Test AC2: PUT sobre msg existente: mensaje actualizado, 200"""
        # Arrange
        conversation_id = "conv-123"
        message_id = "msg-456"
        request_body = {
            "id": message_id,
            "content": "Contenido actualizado",
            "owner": "user-789",
        }

        # Act
        response = await controller.upsert_message(
            conversation_id, message_id, request_body
        )

        # Assert
        assert (
            response.status_code == status.HTTP_201_CREATED
        )  # Mismo código para create/update
        mock_command_handler.handle.assert_called_once()

    @pytest.mark.unit
    async def test_upsert_message_validates_payload(
        self, controller: UpsertMessageController, mock_command_handler: Mock
    ) -> None:
        """Test AC3: PUT con payload inválido → 400"""
        # Arrange
        conversation_id = "conv-123"
        message_id = "msg-456"
        invalid_request_body = {
            "id": message_id,
            "content": "",  # Contenido vacío
            "owner": "user-789",
        }

        # Act
        response = await controller.upsert_message(
            conversation_id, message_id, invalid_request_body
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert b"MessageContent no puede estar vac" in response.body

        # No debe llamar al handler si hay error de validación
        mock_command_handler.handle.assert_not_called()

    @pytest.mark.unit
    async def test_upsert_message_validates_id_consistency(
        self, controller: UpsertMessageController, mock_command_handler: Mock
    ) -> None:
        """Test AC4: Msg id inmutable: cambiar path id ≠ body id → 400"""
        # Arrange
        conversation_id = "conv-123"
        message_id = "msg-456"
        request_body = {
            "id": "msg-different",  # ID diferente al path
            "content": "Contenido",
            "owner": "user-789",
        }

        # Act
        response = await controller.upsert_message(
            conversation_id, message_id, request_body
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert b"Message ID en path y body deben coincidir" in response.body

    @pytest.mark.unit
    async def test_upsert_message_handles_command_handler_error(
        self, controller: UpsertMessageController, mock_command_handler: Mock
    ) -> None:
        """Test manejo de errores del command handler → 500"""
        # Arrange
        conversation_id = "conv-123"
        message_id = "msg-456"
        request_body = {"id": message_id, "content": "Contenido", "owner": "user-789"}

        # Simular error en el handler
        mock_command_handler.handle.side_effect = RuntimeError("Database error")

        # Act
        response = await controller.upsert_message(
            conversation_id, message_id, request_body
        )

        # Assert
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert b"Internal server error" in response.body
