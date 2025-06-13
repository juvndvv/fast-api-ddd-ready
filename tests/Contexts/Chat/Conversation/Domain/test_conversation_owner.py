import pytest

from app.Contexts.Chat.Conversation.Domain.ConversationOwner import ConversationOwner


class TestConversationOwner:
    @pytest.mark.unit
    def test_conversation_owner_creation_with_valid_owner(self) -> None:
        """Test successful creation of ConversationOwner with valid owner"""
        owner = ConversationOwner("user-123")
        assert str(owner) == "user-123"

    @pytest.mark.unit
    def test_conversation_owner_raises_error_for_empty_string(self) -> None:
        """Test that empty string raises ValueError"""
        with pytest.raises(ValueError, match="ConversationOwner no puede estar vacío"):
            ConversationOwner("")

    @pytest.mark.unit
    def test_conversation_owner_raises_error_for_whitespace_only(self) -> None:
        """Test that whitespace-only string raises ValueError"""
        with pytest.raises(ValueError, match="ConversationOwner no puede estar vacío"):
            ConversationOwner("   ")

    @pytest.mark.unit
    def test_conversation_owner_equality(self) -> None:
        """Test ConversationOwner equality comparison"""
        owner1 = ConversationOwner("user-123")
        owner2 = ConversationOwner("user-123")
        owner3 = ConversationOwner("user-456")

        assert owner1 == owner2
        assert owner1 != owner3

    @pytest.mark.unit
    def test_conversation_owner_hash(self) -> None:
        """Test ConversationOwner hash functionality"""
        owner1 = ConversationOwner("user-123")
        owner2 = ConversationOwner("user-123")

        # Should be hashable and equal hashes for equal owners
        assert hash(owner1) == hash(owner2)

        # Should work in sets
        owner_set = {owner1, owner2}
        assert len(owner_set) == 1  # Only one unique owner

    @pytest.mark.unit
    def test_conversation_owner_preserves_whitespace_inside(self) -> None:
        """Test that internal whitespace is preserved"""
        owner = ConversationOwner("user with spaces")
        assert str(owner) == "user with spaces"

    @pytest.mark.unit
    def test_conversation_owner_inequality_with_non_conversation_owner(self) -> None:
        """Test ConversationOwner inequality with non-ConversationOwner objects"""
        owner = ConversationOwner("user-123")

        # Should not be equal to string
        assert owner != "user-123"

        # Should not be equal to None
        assert owner is not None

        # Should not be equal to other types
        assert owner != 123

    @pytest.mark.unit
    def test_conversation_owner_repr(self) -> None:
        """Test ConversationOwner repr method"""
        owner = ConversationOwner("user-123")
        repr_str = repr(owner)
        assert "ConversationOwner" in repr_str
        assert "user-123" in repr_str
