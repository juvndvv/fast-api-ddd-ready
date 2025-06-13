from unittest.mock import Mock

import pytest

from app.Contexts.Chat.Conversation.Domain.Conversation import Conversation
from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId
from app.Contexts.Chat.Conversation.Domain.ConversationOwner import ConversationOwner
from app.Contexts.Chat.Conversation.Infrastructure.Repository.ConversationRepository import (
    ConversationRepository,
)
from app.Contexts.Chat.Message.Application.Create.UpsertMessageCommand import (
    UpsertMessageCommand,
)
from app.Contexts.Chat.Message.Application.Create.UpsertMessageCommandHandler import (
    UpsertMessageCommandHandler,
)
from app.Contexts.Chat.Message.Domain.Message import Message
from app.Contexts.Chat.Message.Domain.MessageChronologyChecker import (
    MessageChronologyChecker,
)
from app.Contexts.Chat.Message.Domain.MessageContent import MessageContent
from app.Contexts.Chat.Message.Domain.MessageId import MessageId
from app.Contexts.Chat.Message.Infrastructure.Repository.MessageRepository import (
    MessageRepository,
)
from app.Contexts.Shared.Application.Bus.Event.EventBus import EventBus


class TestUpsertMessageCommandHandler:
    @pytest.fixture
    def mock_conversation_repo(self) -> Mock:
        return Mock(spec=ConversationRepository)

    @pytest.fixture
    def mock_message_repo(self) -> Mock:
        return Mock(spec=MessageRepository)

    @pytest.fixture
    def mock_chronology_checker(self) -> Mock:
        return Mock(spec=MessageChronologyChecker)

    @pytest.fixture
    def mock_event_bus(self) -> Mock:
        return Mock(spec=EventBus)

    @pytest.fixture
    def handler(
        self,
        mock_conversation_repo: Mock,
        mock_message_repo: Mock,
        mock_chronology_checker: Mock,
        mock_event_bus: Mock,
    ) -> UpsertMessageCommandHandler:
        return UpsertMessageCommandHandler(
            mock_conversation_repo,
            mock_message_repo,
            mock_chronology_checker,
            mock_event_bus,
        )

    @pytest.mark.unit
    async def test_creates_new_conversation_and_message(
        self,
        handler: UpsertMessageCommandHandler,
        mock_conversation_repo: Mock,
        mock_message_repo: Mock,
        mock_chronology_checker: Mock,
        mock_event_bus: Mock,
    ) -> None:
        """Test AC1: Happy path - PUT sobre nueva conv.: conversación y mensaje creados"""
        # Arrange
        command = UpsertMessageCommand(
            conversation_id="conv-123",
            message_id="msg-456",
            content="Hola mundo",
            owner="user-789",
        )

        # No existe la conversación ni el mensaje
        mock_conversation_repo.find_by_id.return_value = None
        mock_message_repo.find_by_id.return_value = None

        # Act
        await handler.handle(command)

        # Assert
        mock_conversation_repo.save.assert_called_once()
        mock_message_repo.save.assert_called_once()
        mock_event_bus.publish.assert_called()

        # Verificar que se crearon los objetos correctos
        saved_conversation = mock_conversation_repo.save.call_args[0][0]
        saved_message = mock_message_repo.save.call_args[0][0]

        assert isinstance(saved_conversation, Conversation)
        assert str(saved_conversation.id) == "conv-123"
        assert str(saved_conversation.owner) == "user-789"

        assert isinstance(saved_message, Message)
        assert str(saved_message.id) == "msg-456"
        assert str(saved_message.content) == "Hola mundo"

    @pytest.mark.unit
    async def test_updates_existing_message_and_truncates_conversation(
        self,
        handler: UpsertMessageCommandHandler,
        mock_conversation_repo: Mock,
        mock_message_repo: Mock,
        mock_chronology_checker: Mock,
        mock_event_bus: Mock,
    ) -> None:
        """Test AC2: Happy path - PUT sobre msg existente: mensaje actualizado, msgs posteriores soft-deleted"""
        # Arrange
        command = UpsertMessageCommand(
            conversation_id="conv-123",
            message_id="msg-456",
            content="Contenido actualizado",
            owner="user-789",
        )

        # Existe conversación y mensaje
        existing_conversation = Conversation.create(
            ConversationId("conv-123"), ConversationOwner("user-789")
        )
        existing_message = Message.create(
            MessageId("msg-456"),
            ConversationId("conv-123"),
            MessageContent("Contenido original"),
        )

        mock_conversation_repo.find_by_id.return_value = existing_conversation
        mock_message_repo.find_by_id.return_value = existing_message

        # Hay mensajes posteriores que deben ser eliminados
        posterior_messages = [MessageId("msg-789"), MessageId("msg-012")]
        mock_chronology_checker.get_messages_after.return_value = posterior_messages

        # Act
        await handler.handle(command)

        # Assert
        mock_conversation_repo.save.assert_called_once()
        mock_message_repo.save.assert_called_once()
        mock_message_repo.soft_delete_messages.assert_called_once_with(
            posterior_messages
        )
        mock_event_bus.publish.assert_called()

        # Verificar que el mensaje fue actualizado
        updated_message = mock_message_repo.save.call_args[0][0]
        assert str(updated_message.content) == "Contenido actualizado"

    @pytest.mark.unit
    async def test_handles_idempotent_operations(
        self,
        handler: UpsertMessageCommandHandler,
        mock_conversation_repo: Mock,
        mock_message_repo: Mock,
        mock_chronology_checker: Mock,
        mock_event_bus: Mock,
    ) -> None:
        """Test AC8: Idempotencia - Repetir PUT con mismos ids y body → estado sin duplicados"""
        # Arrange
        command = UpsertMessageCommand(
            conversation_id="conv-123",
            message_id="msg-456",
            content="Mismo contenido",
            owner="user-789",
        )

        # Existe conversación y mensaje con el mismo contenido
        existing_conversation = Conversation.create(
            ConversationId("conv-123"), ConversationOwner("user-789")
        )
        existing_message = Message.create(
            MessageId("msg-456"),
            ConversationId("conv-123"),
            MessageContent("Mismo contenido"),
        )

        mock_conversation_repo.find_by_id.return_value = existing_conversation
        mock_message_repo.find_by_id.return_value = existing_message
        mock_chronology_checker.get_messages_after.return_value = []

        # Act
        await handler.handle(command)

        # Assert - Solo debe guardar sin duplicar
        mock_conversation_repo.save.assert_called_once()
        mock_message_repo.save.assert_called_once()
        mock_event_bus.publish.assert_called()

    @pytest.mark.unit
    async def test_validates_message_id_consistency(
        self,
        handler: UpsertMessageCommandHandler,
        mock_conversation_repo: Mock,
        mock_message_repo: Mock,
        mock_chronology_checker: Mock,
        mock_event_bus: Mock,
    ) -> None:
        """Test AC4: No-happy path - Msg id inmutable: cambiar path id ≠ body id → 409"""
        # Arrange
        command = UpsertMessageCommand(
            conversation_id="conv-123",
            message_id="msg-456",
            content="Contenido",
            owner="user-789",
        )

        # Existe un mensaje con ID diferente al del comando
        existing_message = Message.create(
            MessageId("msg-different"),
            ConversationId("conv-123"),
            MessageContent("Contenido original"),
        )

        mock_conversation_repo.find_by_id.return_value = None
        mock_message_repo.find_by_id.return_value = existing_message

        # Act & Assert
        with pytest.raises(ValueError, match="Message ID inmutable"):
            await handler.handle(command)
