import pytest

from app.Entrypoint.TestController import TestController


class TestTestController:
    @pytest.fixture
    def controller(self) -> TestController:
        return TestController()

    @pytest.mark.unit
    def test_test_controller_get_router_returns_router(
        self, controller: TestController
    ) -> None:
        """Test that get_router returns a FastAPI router"""
        router = controller.get_router()

        # Should return a router object
        assert router is not None

        # Should have routes registered
        assert len(router.routes) > 0

    @pytest.mark.unit
    def test_test_controller_init_creates_instance(self) -> None:
        """Test that TestController can be instantiated"""
        controller = TestController()
        assert controller is not None
        assert isinstance(controller, TestController)

    @pytest.mark.unit
    def test_get_test_route_returns_hello_world(
        self, controller: TestController
    ) -> None:
        """Test the get_test_route method functionality"""
        response = controller.get_test_route()

        # Should return a response
        assert response is not None

        # Should contain "Hello, World!"
        content = (
            response.body.decode()
            if hasattr(response.body, "decode")
            else str(response.body)
        )
        assert "Hello, World!" in content

        # Should contain a Trace ID
        assert "Trace ID:" in content

    @pytest.mark.unit
    def test_get_test_route_sets_correct_headers(
        self, controller: TestController
    ) -> None:
        """Test that get_test_route sets correct headers"""
        response = controller.get_test_route()

        # Should have correct content type
        assert response.headers["Content-Type"] == "text/plain"

    @pytest.mark.unit
    def test_get_test_route_logs_request(self, controller: TestController) -> None:
        """Test that get_test_route processes request correctly"""
        # This test verifies the method executes without errors
        response = controller.get_test_route()

        # Should return valid response
        assert response is not None
        assert response.status_code == 200
