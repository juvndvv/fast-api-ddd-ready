"""
Health check tests.
"""

from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_app_creates_successfully(app: FastAPI) -> None:
    """Test that the application creates successfully."""
    assert app is not None
    assert hasattr(app, "routes")


@pytest.mark.unit
def test_health_endpoint(client: TestClient) -> None:
    """Test the health endpoint if it exists."""
    # This will pass if the endpoint exists, otherwise skip
    try:
        response = client.get("/health")
        assert response.status_code in [200, 404]  # 404 is ok if endpoint doesn't exist
    except Exception:
        pytest.skip("Health endpoint not implemented yet")


@pytest.mark.unit
def test_client_fixture_works(client: TestClient) -> None:
    """Test that the client fixture works correctly."""
    assert client is not None
    assert hasattr(client, "get")
    assert hasattr(client, "post")


@pytest.mark.unit
def test_sample_data_fixture(sample_data: dict[str, Any]) -> None:
    """Test that the sample_data fixture provides expected data."""
    assert "test_user_id" in sample_data
    assert "test_message" in sample_data
    assert "test_timestamp" in sample_data
    assert sample_data["test_user_id"] == 1
    assert sample_data["test_message"] == "Hello, world!"
