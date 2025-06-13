from datetime import datetime

import pytest

from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId
from app.Contexts.Chat.Message.Domain.Message import Message
from app.Contexts.Chat.Message.Domain.MessageContent import MessageContent
from app.Contexts.Chat.Message.Domain.MessageId import MessageId


class TestMessage:
    @pytest.mark.unit
    def test_message_creation(self) -> None:
        """Test que un mensaje se crea correctamente"""
        message_id = MessageId("msg-123")
        conversation_id = ConversationId("conv-456")
        content = MessageContent("Hola mundo")

        message = Message.create(message_id, conversation_id, content)

        assert message.id == message_id
        assert message.conversation_id == conversation_id
        assert message.content == content
        assert isinstance(message.created_at, datetime)
        assert isinstance(message.updated_at, datetime)
        assert message.created_at == message.updated_at
        assert not message.is_deleted

    @pytest.mark.unit
    def test_message_update_content(self) -> None:
        """Test que un mensaje actualiza su contenido"""
        message_id = MessageId("msg-123")
        conversation_id = ConversationId("conv-456")
        original_content = MessageContent("Hola mundo")
        new_content = MessageContent("Hola mundo actualizado")

        message = Message.create(message_id, conversation_id, original_content)
        original_updated_at = message.updated_at

        message.update_content(new_content)

        assert message.content == new_content
        assert message.updated_at > original_updated_at

    @pytest.mark.unit
    def test_message_soft_delete(self) -> None:
        """Test que un mensaje se marca como eliminado (soft delete)"""
        message_id = MessageId("msg-123")
        conversation_id = ConversationId("conv-456")
        content = MessageContent("Hola mundo")

        message = Message.create(message_id, conversation_id, content)
        original_updated_at = message.updated_at

        message.soft_delete()

        assert message.is_deleted
        assert message.updated_at > original_updated_at

    @pytest.mark.unit
    def test_message_equality(self) -> None:
        """Test que dos mensajes son iguales por ID"""
        message_id = MessageId("msg-123")
        conversation_id = ConversationId("conv-456")
        content = MessageContent("Hola mundo")

        message1 = Message.create(message_id, conversation_id, content)
        message2 = Message.create(message_id, conversation_id, content)

        assert message1 == message2
        assert hash(message1) == hash(message2)

    @pytest.mark.unit
    def test_message_events_on_creation(self) -> None:
        """Test que se publican eventos de dominio al crear mensaje"""
        message_id = MessageId("msg-123")
        conversation_id = ConversationId("conv-456")
        content = MessageContent("Hola mundo")

        message = Message.create(message_id, conversation_id, content)
        events = message.domain_events

        assert len(events) == 1
        assert events[0].name == "message.created"
        assert events[0].payload["message_id"] == "msg-123"
        assert events[0].payload["conversation_id"] == "conv-456"

    @pytest.mark.unit
    def test_message_events_on_update(self) -> None:
        """Test que se publican eventos de dominio al actualizar mensaje"""
        message_id = MessageId("msg-123")
        conversation_id = ConversationId("conv-456")
        original_content = MessageContent("Hola mundo")
        new_content = MessageContent("Hola mundo actualizado")

        message = Message.create(message_id, conversation_id, original_content)
        message.clear_domain_events()  # Limpiar eventos de creación

        message.update_content(new_content)
        events = message.domain_events

        assert len(events) == 1
        assert events[0].name == "message.updated"
        assert events[0].payload["message_id"] == "msg-123"
        assert events[0].payload["conversation_id"] == "conv-456"
