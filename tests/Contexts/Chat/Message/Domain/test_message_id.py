import pytest

from app.Contexts.Chat.Message.Domain.MessageId import MessageId


class TestMessageId:
    @pytest.mark.unit
    def test_message_id_creation_with_valid_id(self) -> None:
        """Test successful creation of MessageId with valid ID"""
        message_id = MessageId("msg-123")
        assert str(message_id) == "msg-123"

    @pytest.mark.unit
    def test_message_id_raises_error_for_empty_string(self) -> None:
        """Test that empty string raises ValueError"""
        with pytest.raises(ValueError, match="MessageId no puede estar vacío"):
            MessageId("")

    @pytest.mark.unit
    def test_message_id_raises_error_for_whitespace_only(self) -> None:
        """Test that whitespace-only string raises ValueError"""
        with pytest.raises(ValueError, match="MessageId no puede estar vacío"):
            MessageId("   ")

    @pytest.mark.unit
    def test_message_id_equality(self) -> None:
        """Test MessageId equality comparison"""
        id1 = MessageId("msg-123")
        id2 = MessageId("msg-123")
        id3 = MessageId("msg-456")

        assert id1 == id2
        assert id1 != id3

    @pytest.mark.unit
    def test_message_id_hash(self) -> None:
        """Test MessageId hash functionality"""
        id1 = MessageId("msg-123")
        id2 = MessageId("msg-123")

        # Should be hashable and equal hashes for equal IDs
        assert hash(id1) == hash(id2)

        # Should work in sets
        id_set = {id1, id2}
        assert len(id_set) == 1  # Only one unique ID

    @pytest.mark.unit
    def test_message_id_inequality_with_non_message_id(self) -> None:
        """Test MessageId inequality with non-MessageId objects"""
        msg_id = MessageId("msg-123")

        # Should not be equal to string
        assert msg_id != "msg-123"

        # Should not be equal to None
        assert msg_id is not None

        # Should not be equal to other types
        assert msg_id != 123

    @pytest.mark.unit
    def test_message_id_repr(self) -> None:
        """Test MessageId repr method"""
        msg_id = MessageId("msg-123")
        repr_str = repr(msg_id)
        assert "MessageId" in repr_str
        assert "msg-123" in repr_str
