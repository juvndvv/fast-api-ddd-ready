from abc import ABC

import pytest

from app.Contexts.Chat.Conversation.Infrastructure.Repository.ConversationRepository import (
    ConversationRepository,
)


class TestConversationRepository:
    @pytest.mark.unit
    def test_is_abstract_base_class(self) -> None:
        """Test que ConversationRepository es una clase base abstracta"""
        assert issubclass(ConversationRepository, ABC)

        # Verificar que no se puede instanciar directamente
        with pytest.raises(TypeError):
            ConversationRepository()  # type: ignore
