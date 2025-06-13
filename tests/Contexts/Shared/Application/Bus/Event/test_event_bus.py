import pytest

from app.Contexts.Shared.Application.Bus.Event.EventBus import EventBus


class TestEventBus:
    @pytest.mark.unit
    def test_event_bus_is_abstract(self) -> None:
        """Test that EventBus is an abstract class"""
        # Should not be able to instantiate directly
        with pytest.raises(TypeError):
            EventBus()  # type: ignore[abstract]
