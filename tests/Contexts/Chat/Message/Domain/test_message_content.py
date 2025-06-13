import pytest

from app.Contexts.Chat.Message.Domain.MessageContent import MessageContent


class TestMessageContent:
    @pytest.mark.unit
    def test_message_content_creation_with_valid_content(self) -> None:
        """Test successful creation of MessageContent with valid content"""
        content = MessageContent("Hola mundo")
        assert str(content) == "Hola mundo"

    @pytest.mark.unit
    def test_message_content_strips_whitespace(self) -> None:
        """Test that MessageContent strips surrounding whitespace"""
        content = MessageContent("  Hola mundo  ")
        assert str(content) == "Hola mundo"

    @pytest.mark.unit
    def test_message_content_raises_error_for_empty_string(self) -> None:
        """Test that empty string raises ValueError"""
        with pytest.raises(ValueError, match="MessageContent no puede estar vacío"):
            MessageContent("")

    @pytest.mark.unit
    def test_message_content_raises_error_for_whitespace_only(self) -> None:
        """Test that whitespace-only string raises ValueError"""
        with pytest.raises(ValueError, match="MessageContent no puede estar vacío"):
            MessageContent("   ")

    @pytest.mark.unit
    def test_message_content_equality(self) -> None:
        """Test MessageContent equality comparison"""
        content1 = MessageContent("Hola mundo")
        content2 = MessageContent("Hola mundo")
        content3 = MessageContent("Otro contenido")

        assert content1 == content2
        assert content1 != content3

    @pytest.mark.unit
    def test_message_content_hash(self) -> None:
        """Test MessageContent hash functionality"""
        content1 = MessageContent("Hola mundo")
        content2 = MessageContent("Hola mundo")

        # Should be hashable and equal hashes for equal content
        assert hash(content1) == hash(content2)

        # Should work in sets
        content_set = {content1, content2}
        assert len(content_set) == 1  # Only one unique content

    @pytest.mark.unit
    def test_message_content_inequality_with_non_message_content(self) -> None:
        """Test MessageContent inequality with non-MessageContent objects"""
        content = MessageContent("Hola mundo")

        # Should not be equal to string
        assert content != "Hola mundo"

        # Should not be equal to None
        assert content is not None

        # Should not be equal to other types
        assert content != 123

    @pytest.mark.unit
    def test_message_content_repr(self) -> None:
        """Test MessageContent repr method"""
        content = MessageContent("Hola mundo")
        repr_str = repr(content)
        assert "MessageContent" in repr_str
        assert "Hola mundo" in repr_str
