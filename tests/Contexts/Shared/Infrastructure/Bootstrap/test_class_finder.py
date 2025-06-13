import pytest

from app.Contexts.Shared.Infrastructure.Bootstrap.ClassFinder import ClassFinder
from app.Contexts.Shared.Infrastructure.Module.ApplicationModule import (
    ApplicationModule,
)


class TestClassFinder:
    @pytest.mark.unit
    def test_find_returns_modules_matching_criteria(self) -> None:
        """Test that find returns modules that match the base class and suffix"""
        # Use ApplicationModule which is a concrete class that works with ClassFinder
        modules = ClassFinder.find(ApplicationModule, "Module")  # type: ignore[arg-type]

        # Should find at least ChatModule
        module_names = [m.__name__ for m in modules]
        assert "ChatModule" in module_names

    @pytest.mark.unit
    def test_find_returns_empty_list_for_non_existent_suffix(self) -> None:
        """Test that find returns empty list when no classes match suffix"""
        result = ClassFinder.find(ApplicationModule, "NonExistentSuffix")  # type: ignore[arg-type]
        assert result == []
