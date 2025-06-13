import pytest
from fastapi import APIRouter

from app.Contexts.Shared.Infrastructure.Http.Controller import Controller


class ConcreteController(Controller):
    """Concrete implementation for testing"""

    def get_router(self) -> APIRouter:
        return APIRouter()


class TestController:
    @pytest.mark.unit
    def test_controller_is_abstract(self) -> None:
        """Test that Controller is an abstract class"""
        # Should not be able to instantiate directly
        with pytest.raises(TypeError):
            Controller()  # type: ignore[abstract]

    @pytest.mark.unit
    def test_concrete_controller_can_be_instantiated(self) -> None:
        """Test that concrete controller implementation works"""
        controller = ConcreteController()
        assert controller is not None
        assert isinstance(controller, Controller)

    @pytest.mark.unit
    def test_concrete_controller_has_get_router(self) -> None:
        """Test that concrete controller implements get_router"""
        controller = ConcreteController()
        router = controller.get_router()
        assert router is not None
