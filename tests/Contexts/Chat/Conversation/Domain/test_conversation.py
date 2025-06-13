from datetime import datetime

import pytest

from app.Contexts.Chat.Conversation.Domain.Conversation import Conversation
from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId
from app.Contexts.Chat.Conversation.Domain.ConversationOwner import ConversationOwner
from app.Contexts.Chat.Message.Domain.MessageId import MessageId


class TestConversation:
    @pytest.mark.unit
    def test_conversation_creation(self) -> None:
        """Test que una conversación se crea con metadatos mínimos"""
        conversation_id = ConversationId("conv-123")
        owner = ConversationOwner("user-456")

        conversation = Conversation.create(conversation_id, owner)

        assert conversation.id == conversation_id
        assert conversation.owner == owner
        assert conversation.last_message_id is None
        assert isinstance(conversation.created_at, datetime)
        assert isinstance(conversation.updated_at, datetime)
        assert conversation.created_at == conversation.updated_at

    @pytest.mark.unit
    def test_conversation_update_last_message(self) -> None:
        """Test que una conversación actualiza su último mensaje"""
        conversation_id = ConversationId("conv-123")
        owner = ConversationOwner("user-456")
        message_id = MessageId("msg-789")

        conversation = Conversation.create(conversation_id, owner)
        original_updated_at = conversation.updated_at

        conversation.update_last_message(message_id)

        assert conversation.last_message_id == message_id
        assert conversation.updated_at > original_updated_at

    @pytest.mark.unit
    def test_conversation_equality(self) -> None:
        """Test que dos conversaciones son iguales por ID"""
        conversation_id = ConversationId("conv-123")
        owner = ConversationOwner("user-456")

        conversation1 = Conversation.create(conversation_id, owner)
        conversation2 = Conversation.create(conversation_id, owner)

        assert conversation1 == conversation2
        assert hash(conversation1) == hash(conversation2)

    @pytest.mark.unit
    def test_conversation_inequality(self) -> None:
        """Test que dos conversaciones con diferente ID no son iguales"""
        owner = ConversationOwner("user-456")

        conversation1 = Conversation.create(ConversationId("conv-123"), owner)
        conversation2 = Conversation.create(ConversationId("conv-456"), owner)

        assert conversation1 != conversation2
        assert hash(conversation1) != hash(conversation2)

    @pytest.mark.unit
    def test_conversation_events_on_creation(self) -> None:
        """Test que se publican eventos de dominio al crear conversación"""
        conversation_id = ConversationId("conv-123")
        owner = ConversationOwner("user-456")

        conversation = Conversation.create(conversation_id, owner)
        events = conversation.domain_events

        assert len(events) == 1
        assert events[0].name == "conversation.created"
        assert events[0].payload["conversation_id"] == "conv-123"
        assert events[0].payload["owner"] == "user-456"
