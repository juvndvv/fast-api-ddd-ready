import pytest

from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId
from app.Contexts.Chat.Infrastructure.Repository.InMemoryMessageRepository import (
    InMemoryMessageRepository,
)
from app.Contexts.Chat.Message.Domain.Message import Message
from app.Contexts.Chat.Message.Domain.MessageContent import MessageContent
from app.Contexts.Chat.Message.Domain.MessageId import MessageId


class TestInMemoryMessageRepository:
    @pytest.fixture
    def repository(self) -> InMemoryMessageRepository:
        return InMemoryMessageRepository()

    @pytest.fixture
    def sample_message(self) -> Message:
        return Message.create(
            MessageId("msg-123"),
            ConversationId("conv-456"),
            MessageContent("Test message content"),
        )

    @pytest.mark.unit
    def test_find_by_id_returns_none_when_message_not_found(
        self, repository: InMemoryMessageRepository
    ) -> None:
        """Test that find_by_id returns None when message doesn't exist"""
        result = repository.find_by_id(MessageId("non-existent"))
        assert result is None

    @pytest.mark.unit
    def test_find_by_id_returns_message_when_found(
        self, repository: InMemoryMessageRepository, sample_message: Message
    ) -> None:
        """Test that find_by_id returns message when it exists"""
        # Save message first
        repository.save(sample_message)

        # Find it
        result = repository.find_by_id(MessageId("msg-123"))
        assert result is not None
        assert result.id == MessageId("msg-123")

    @pytest.mark.unit
    def test_save_stores_message(
        self, repository: InMemoryMessageRepository, sample_message: Message
    ) -> None:
        """Test that save stores the message"""
        repository.save(sample_message)

        result = repository.find_by_id(MessageId("msg-123"))
        assert result is not None
        assert result == sample_message

    @pytest.mark.unit
    def test_find_messages_after_returns_empty_list(
        self, repository: InMemoryMessageRepository
    ) -> None:
        """Test that find_messages_after returns empty list (simple implementation)"""
        result = repository.find_messages_after(
            ConversationId("conv-123"), MessageId("msg-456")
        )
        assert result == []

    @pytest.mark.unit
    def test_soft_delete_messages_marks_messages_as_deleted(
        self, repository: InMemoryMessageRepository, sample_message: Message
    ) -> None:
        """Test that soft_delete_messages marks messages as deleted"""
        # Save message first
        repository.save(sample_message)

        # Soft delete it
        repository.soft_delete_messages([MessageId("msg-123")])

        # Message should still exist but be marked as deleted
        result = repository.find_by_id(MessageId("msg-123"))
        assert result is not None
        assert result.is_deleted is True

    @pytest.mark.unit
    def test_soft_delete_messages_ignores_non_existent_messages(
        self, repository: InMemoryMessageRepository
    ) -> None:
        """Test that soft_delete_messages doesn't fail on non-existent messages"""
        # Should not raise any exception
        repository.soft_delete_messages([MessageId("non-existent")])

    @pytest.mark.unit
    def test_paginate_messages_returns_empty_for_non_existent_conversation(
        self, repository: InMemoryMessageRepository
    ) -> None:
        """Test that paginate_messages returns empty list for non-existent conversation"""
        result = repository.paginate_messages(
            ConversationId("conv-nonexistent"), None, 10
        )
        assert result == []

    @pytest.mark.unit
    def test_paginate_messages_filters_by_conversation_id(
        self, repository: InMemoryMessageRepository
    ) -> None:
        """Test that paginate_messages filters by conversation ID"""
        # Create messages in different conversations
        msg1 = Message.create(
            MessageId("msg-1"), ConversationId("conv-1"), MessageContent("Message 1")
        )
        msg2 = Message.create(
            MessageId("msg-2"), ConversationId("conv-2"), MessageContent("Message 2")
        )

        repository.save(msg1)
        repository.save(msg2)

        # Get messages for conv-1 only
        result = repository.paginate_messages(ConversationId("conv-1"), None, 10)

        assert len(result) == 1
        assert result[0].id == MessageId("msg-1")

    @pytest.mark.unit
    def test_paginate_messages_excludes_deleted_messages(
        self, repository: InMemoryMessageRepository
    ) -> None:
        """Test that paginate_messages excludes deleted messages"""
        # Create and save a message
        msg = Message.create(
            MessageId("msg-1"), ConversationId("conv-1"), MessageContent("Message 1")
        )
        repository.save(msg)

        # Soft delete it
        repository.soft_delete_messages([MessageId("msg-1")])

        # Should not appear in pagination
        result = repository.paginate_messages(ConversationId("conv-1"), None, 10)
        assert len(result) == 0

    @pytest.mark.unit
    def test_paginate_messages_respects_limit(
        self, repository: InMemoryMessageRepository
    ) -> None:
        """Test that paginate_messages respects the limit parameter"""
        # Create multiple messages
        for i in range(5):
            msg = Message.create(
                MessageId(f"msg-{i}"),
                ConversationId("conv-1"),
                MessageContent(f"Message {i}"),
            )
            repository.save(msg)

        # Request only 3 messages
        result = repository.paginate_messages(ConversationId("conv-1"), None, 3)
        assert len(result) == 3

    @pytest.mark.unit
    def test_paginate_messages_with_cursor_starts_after_cursor(
        self, repository: InMemoryMessageRepository
    ) -> None:
        """Test that paginate_messages with cursor starts after the cursor message"""
        # Create multiple messages (they'll be sorted by ID)
        for i in range(5):
            msg = Message.create(
                MessageId(f"msg-{i:03d}"),  # Zero-padded for proper sorting
                ConversationId("conv-1"),
                MessageContent(f"Message {i}"),
            )
            repository.save(msg)

        # Request messages after msg-002
        result = repository.paginate_messages(ConversationId("conv-1"), "msg-002", 10)

        # Should get msg-003 and msg-004 (messages after the cursor)
        assert len(result) == 2
        assert result[0].id == MessageId("msg-003")
        assert result[1].id == MessageId("msg-004")
