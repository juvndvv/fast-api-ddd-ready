import pytest

from app.Contexts.Shared.Application.Bus.Query.QueryBus import QueryBus


class TestQueryBus:
    @pytest.mark.unit
    def test_query_bus_is_abstract(self) -> None:
        """Test that QueryBus is an abstract class"""
        # Should not be able to instantiate directly
        with pytest.raises(TypeError):
            QueryBus()  # type: ignore[abstract]
