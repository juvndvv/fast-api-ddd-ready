"""
Global test configuration for pytest.
"""

from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.Contexts.Shared.Infrastructure.Bootstrap.ApplicationBootstrapper import (
    ApplicationBootstrapper,
)


@pytest.fixture
def app() -> FastAPI:
    """Create a FastAPI application instance for testing."""
    bootstrapper = ApplicationBootstrapper()
    return bootstrapper.app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def sample_data() -> dict[str, Any]:
    """Provide sample data for tests."""
    return {
        "test_user_id": 1,
        "test_message": "Hello, world!",
        "test_timestamp": "2024-01-01T00:00:00Z",
    }
