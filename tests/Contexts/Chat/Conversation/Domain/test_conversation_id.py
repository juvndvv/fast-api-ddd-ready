import pytest

from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId


class TestConversationId:
    @pytest.mark.unit
    def test_conversation_id_creation_with_valid_id(self) -> None:
        """Test successful creation of ConversationId with valid ID"""
        conversation_id = ConversationId("conv-123")
        assert str(conversation_id) == "conv-123"

    @pytest.mark.unit
    def test_conversation_id_raises_error_for_empty_string(self) -> None:
        """Test that empty string raises ValueError"""
        with pytest.raises(ValueError, match="ConversationId no puede estar vacío"):
            ConversationId("")

    @pytest.mark.unit
    def test_conversation_id_raises_error_for_whitespace_only(self) -> None:
        """Test that whitespace-only string raises ValueError"""
        with pytest.raises(ValueError, match="ConversationId no puede estar vacío"):
            ConversationId("   ")

    @pytest.mark.unit
    def test_conversation_id_equality(self) -> None:
        """Test ConversationId equality comparison"""
        id1 = ConversationId("conv-123")
        id2 = ConversationId("conv-123")
        id3 = ConversationId("conv-456")

        assert id1 == id2
        assert id1 != id3

    @pytest.mark.unit
    def test_conversation_id_hash(self) -> None:
        """Test ConversationId hash functionality"""
        id1 = ConversationId("conv-123")
        id2 = ConversationId("conv-123")

        # Should be hashable and equal hashes for equal IDs
        assert hash(id1) == hash(id2)

        # Should work in sets
        id_set = {id1, id2}
        assert len(id_set) == 1  # Only one unique ID

    @pytest.mark.unit
    def test_conversation_id_inequality_with_non_conversation_id(self) -> None:
        """Test ConversationId inequality with non-ConversationId objects"""
        conv_id = ConversationId("conv-123")

        # Should not be equal to string
        assert conv_id != "conv-123"

        # Should not be equal to None
        assert conv_id is not None

        # Should not be equal to other types
        assert conv_id != 123

    @pytest.mark.unit
    def test_conversation_id_repr(self) -> None:
        """Test ConversationId repr method"""
        conv_id = ConversationId("conv-123")
        repr_str = repr(conv_id)
        assert "ConversationId" in repr_str
        assert "conv-123" in repr_str
