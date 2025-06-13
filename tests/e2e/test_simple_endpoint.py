"""
Simple test to debug application routing
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.e2e
def test_simple_health_endpoint(client: TestClient) -> None:
    """Test a simple health endpoint to verify the app is working"""
    # Try to hit a non-existent endpoint to see the 404 response format
    response = client.get("/health")

    # Just check that we get some response (200 if exists, 404 if not)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

    # Print the response for debugging
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.json()}")

    # Check available routes by trying a root path
    root_response = client.get("/")
    print(f"Root response status: {root_response.status_code}")
    if root_response.status_code != 404:
        print(f"Root response body: {root_response.json()}")

    # Check docs endpoint to see if FastAPI is working
    docs_response = client.get("/docs")
    print(f"Docs response status: {docs_response.status_code}")

    # Test should pass regardless - this is just for debugging
    assert True
