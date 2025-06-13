from unittest.mock import patch

import pytest

from app.Contexts.Shared.Infrastructure.Settings.KafkaSettings import KafkaSettings


class TestKafkaSettings:
    @pytest.mark.unit
    def test_kafka_settings_creation_with_required_params(self) -> None:
        """Test KafkaSettings creation with required parameters"""
        settings = KafkaSettings(
            bootstrap_servers=["localhost:9092"],
            topics_prefix="test",
            consumer_group_id="test-group",
        )

        # Check required values
        assert settings.bootstrap_servers == ["localhost:9092"]
        assert settings.topics_prefix == "test"
        assert settings.consumer_group_id == "test-group"

        # Check default values
        assert settings.enable_auto_commit is True
        assert settings.auto_offset_reset == "earliest"
        assert settings.max_poll_records == 500

    @pytest.mark.unit
    @patch.dict(
        "os.environ",
        {
            "KAFKA_BOOTSTRAP_SERVERS": "custom-server:9092",
            "KAFKA_TOPICS_PREFIX": "custom",
            "KAFKA_CONSUMER_GROUP_ID": "custom-group",
            "KAFKA_AUTO_OFFSET_RESET": "latest",
            "KAFKA_ENABLE_AUTO_COMMIT": "false",
            "KAFKA_MAX_POLL_RECORDS": "100",
        },
    )
    def test_kafka_settings_from_env(self) -> None:
        """Test KafkaSettings.from_env() reads from environment variables"""
        settings = KafkaSettings.from_env()

        # Check environment values are loaded
        assert settings.bootstrap_servers == ["custom-server:9092"]
        assert settings.topics_prefix == "custom"
        assert settings.consumer_group_id == "custom-group"
        assert settings.auto_offset_reset == "latest"
        assert settings.enable_auto_commit is False
        assert settings.max_poll_records == 100

    @pytest.mark.unit
    def test_kafka_settings_from_env_default_values(self) -> None:
        """Test KafkaSettings.from_env() uses default values when env vars not set"""
        settings = KafkaSettings.from_env()

        # Check default values
        assert settings.bootstrap_servers == ["localhost:9092"]
        assert settings.topics_prefix == "yurest"
        assert settings.consumer_group_id == "yurest-app"
        assert settings.auto_offset_reset == "earliest"
        assert settings.enable_auto_commit is True
        assert settings.max_poll_records == 500

    @pytest.mark.unit
    def test_kafka_settings_get_topic_name(self) -> None:
        """Test KafkaSettings.get_topic_name() method"""
        settings = KafkaSettings(
            bootstrap_servers=["localhost:9092"],
            topics_prefix="test",
            consumer_group_id="test-group",
        )

        # Test topic name generation
        topic_name = settings.get_topic_name("user.created")
        assert topic_name == "test.user_created"

        # Test with different event name
        topic_name = settings.get_topic_name("order.payment.processed")
        assert topic_name == "test.order_payment_processed"
