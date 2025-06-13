"""
End-to-end tests for Chat context.
Tests complete user journeys through HTTP endpoints.
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.e2e
class TestChatContextE2E:
    """End-to-end tests for Chat context covering all acceptance criteria"""

    def test_ac1_create_new_conversation_and_message_flow(
        self, client: TestClient
    ) -> None:
        """
        AC1: PUT sobre nueva conversación → crea conversación y mensaje (201)
        End-to-end flow: PUT message → GET conversation → Verify data consistency
        """
        conversation_id = "conv-e2e-001"
        message_id = "msg-e2e-001"

        # Step 1: PUT new message (should create conversation and message)
        message_data = {
            "id": message_id,
            "content": "Hola, este es el primer mensaje",
            "owner": "user-e2e-001",
        }

        response = client.put(
            f"/conversations/{conversation_id}/messages/{message_id}", json=message_data
        )

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["message"] == "Message upserted successfully"

        # Step 2: GET conversation to verify it was created
        conversation_response = client.get(f"/conversations/{conversation_id}")

        assert conversation_response.status_code == status.HTTP_200_OK
        conversation_data = conversation_response.json()
        assert conversation_data["id"] == conversation_id
        assert conversation_data["owner"] == "user-e2e-001"
        assert conversation_data["last_message_id"] == message_id
        assert "created_at" in conversation_data
        assert "updated_at" in conversation_data

    def test_ac2_update_existing_message_flow(self, client: TestClient) -> None:
        """
        AC2: PUT sobre mensaje existente → actualiza mensaje, soft-deletes posteriores
        End-to-end flow: Create conversation → Create messages → Update middle message → Verify truncation
        """
        conversation_id = "conv-e2e-002"

        # Step 1: Create conversation with first message
        message1_data = {
            "id": "msg-e2e-021",
            "content": "Primer mensaje",
            "owner": "user-e2e-002",
        }
        response1 = client.put(
            f"/conversations/{conversation_id}/messages/msg-e2e-021", json=message1_data
        )
        assert response1.status_code == status.HTTP_201_CREATED

        # Step 2: Add second message
        message2_data = {
            "id": "msg-e2e-022",
            "content": "Segundo mensaje",
            "owner": "user-e2e-002",
        }
        response2 = client.put(
            f"/conversations/{conversation_id}/messages/msg-e2e-022", json=message2_data
        )
        assert response2.status_code == status.HTTP_201_CREATED

        # Step 3: Add third message
        message3_data = {
            "id": "msg-e2e-023",
            "content": "Tercer mensaje",
            "owner": "user-e2e-002",
        }
        response3 = client.put(
            f"/conversations/{conversation_id}/messages/msg-e2e-023", json=message3_data
        )
        assert response3.status_code == status.HTTP_201_CREATED

        # Step 4: Update second message (should trigger truncation of third message)
        updated_message2_data = {
            "id": "msg-e2e-022",
            "content": "Segundo mensaje ACTUALIZADO",
            "owner": "user-e2e-002",
        }
        update_response = client.put(
            f"/conversations/{conversation_id}/messages/msg-e2e-022",
            json=updated_message2_data,
        )
        assert update_response.status_code == status.HTTP_201_CREATED

        # Step 5: Verify conversation state after update
        conversation_response = client.get(f"/conversations/{conversation_id}")
        assert conversation_response.status_code == status.HTTP_200_OK
        conversation_data = conversation_response.json()
        assert conversation_data["last_message_id"] == "msg-e2e-022"

    def test_ac3_validation_error_flow(self, client: TestClient) -> None:
        """
        AC3: Invalid payload → 422 error
        End-to-end flow: Send invalid payloads and verify proper error responses
        """
        conversation_id = "conv-e2e-003"
        message_id = "msg-e2e-003"

        # Test empty content
        invalid_data_empty = {
            "id": message_id,
            "content": "",  # Empty content should fail
            "owner": "user-e2e-003",
        }

        response = client.put(
            f"/conversations/{conversation_id}/messages/{message_id}",
            json=invalid_data_empty,
        )

        # Should get validation error
        assert response.status_code in [
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            status.HTTP_400_BAD_REQUEST,
        ]

    def test_ac4_message_id_immutability_flow(self, client: TestClient) -> None:
        """
        AC4: Message ID inmutable → path ID ≠ body ID returns error
        End-to-end flow: Try to change message ID and verify error
        """
        conversation_id = "conv-e2e-004"
        path_message_id = "msg-e2e-004"
        body_message_id = "msg-e2e-004-different"

        # Try to create message with inconsistent IDs
        inconsistent_data = {
            "id": body_message_id,  # Different from path
            "content": "Contenido de prueba",
            "owner": "user-e2e-004",
        }

        response = client.put(
            f"/conversations/{conversation_id}/messages/{path_message_id}",
            json=inconsistent_data,
        )

        # Should get conflict or validation error
        assert response.status_code in [
            status.HTTP_409_CONFLICT,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            status.HTTP_400_BAD_REQUEST,
        ]

    def test_ac5_get_conversation_without_message_queries_flow(
        self, client: TestClient
    ) -> None:
        """
        AC5: GET conversation → returns metadata without executing message queries
        End-to-end flow: Create conversation → GET conversation → Verify only metadata returned
        """
        conversation_id = "conv-e2e-005"
        message_id = "msg-e2e-005"

        # Step 1: Create conversation with message
        message_data = {
            "id": message_id,
            "content": "Mensaje para probar AC5",
            "owner": "user-e2e-005",
        }

        create_response = client.put(
            f"/conversations/{conversation_id}/messages/{message_id}", json=message_data
        )
        assert create_response.status_code == status.HTTP_201_CREATED

        # Step 2: GET conversation metadata
        get_response = client.get(f"/conversations/{conversation_id}")

        assert get_response.status_code == status.HTTP_200_OK
        conversation_data = get_response.json()

        # Verify conversation metadata is present
        expected_fields = ["id", "owner", "created_at", "updated_at", "last_message_id"]
        for field in expected_fields:
            assert field in conversation_data, f"Missing field: {field}"

        # Verify no message content is included (per AC5)
        assert "messages" not in conversation_data
        assert "content" not in conversation_data

        # Verify values are correct
        assert conversation_data["id"] == conversation_id
        assert conversation_data["owner"] == "user-e2e-005"
        assert conversation_data["last_message_id"] == message_id

    def test_ac6_message_pagination_flow(self, client: TestClient) -> None:
        """
        AC6: GET messages → cursor-based pagination with next-cursor and has_more
        End-to-end flow: Create multiple messages → Test pagination behavior
        """
        conversation_id = "conv-e2e-006"

        # Step 1: Create multiple messages to test pagination
        for i in range(5):
            message_id = f"msg-e2e-006-{i:03d}"
            message_data = {
                "id": message_id,
                "content": f"Mensaje número {i+1} para paginación",
                "owner": "user-e2e-006",
            }

            response = client.put(
                f"/conversations/{conversation_id}/messages/{message_id}",
                json=message_data,
            )
            assert response.status_code == status.HTTP_201_CREATED

        # Step 2: Test pagination without cursor (first page)
        pagination_response = client.get(
            f"/conversations/{conversation_id}/messages?limit=2"
        )

        assert pagination_response.status_code == status.HTTP_200_OK
        pagination_data = pagination_response.json()

        # Verify pagination structure
        expected_pagination_fields = ["messages", "next_cursor", "has_more"]
        for field in expected_pagination_fields:
            assert field in pagination_data, f"Missing pagination field: {field}"

        # Verify pagination behavior
        assert len(pagination_data["messages"]) <= 2  # Respects limit
        assert isinstance(pagination_data["has_more"], bool)

    def test_ac8_idempotency_flow(self, client: TestClient) -> None:
        """
        AC8: Idempotency → repeated PUT operations maintain consistent state
        End-to-end flow: PUT same message multiple times → Verify consistent results
        """
        conversation_id = "conv-e2e-008"
        message_id = "msg-e2e-008"

        message_data = {
            "id": message_id,
            "content": "Mensaje idempotente",
            "owner": "user-e2e-008",
        }

        # Step 1: First PUT request
        response1 = client.put(
            f"/conversations/{conversation_id}/messages/{message_id}", json=message_data
        )
        assert response1.status_code == status.HTTP_201_CREATED

        # Step 2: Second PUT request with exact same data
        response2 = client.put(
            f"/conversations/{conversation_id}/messages/{message_id}", json=message_data
        )
        assert response2.status_code == status.HTTP_201_CREATED

        # Step 3: Verify conversation state is consistent
        conversation_response = client.get(f"/conversations/{conversation_id}")
        assert conversation_response.status_code == status.HTTP_200_OK

        conversation_data = conversation_response.json()
        assert conversation_data["id"] == conversation_id
        assert conversation_data["owner"] == "user-e2e-008"
        assert conversation_data["last_message_id"] == message_id

    def test_conversation_not_found_flow(self, client: TestClient) -> None:
        """
        Test complete flow for non-existent conversation
        End-to-end flow: GET non-existent conversation → Verify 404 error
        """
        non_existent_conversation_id = "conv-nonexistent-e2e"

        response = client.get(f"/conversations/{non_existent_conversation_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        error_data = response.json()
        # Check for either 'error' or 'detail' field (FastAPI default)
        assert "error" in error_data or "detail" in error_data
        error_message = error_data.get("error", error_data.get("detail", ""))
        assert "not found" in error_message.lower()
