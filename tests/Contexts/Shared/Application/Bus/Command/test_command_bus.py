import pytest

from app.Contexts.Shared.Application.Bus.Command.CommandBus import CommandBus


class TestCommandBus:
    @pytest.mark.unit
    def test_command_bus_is_abstract(self) -> None:
        """Test that CommandBus is an abstract class"""
        # Should not be able to instantiate directly
        with pytest.raises(TypeError):
            CommandBus()  # type: ignore[abstract]
