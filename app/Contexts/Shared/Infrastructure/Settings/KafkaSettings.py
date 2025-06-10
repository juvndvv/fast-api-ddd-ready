import os
from dataclasses import dataclass


@dataclass
class KafkaSettings:
    bootstrap_servers: list[str]
    topics_prefix: str
    consumer_group_id: str
    enable_auto_commit: bool = True
    auto_offset_reset: str = "earliest"
    max_poll_records: int = 500
    session_timeout_ms: int = 30000
    heartbeat_interval_ms: int = 3000
    enabled: bool = True  # Nueva configuración para habilitar/deshabilitar Kafka

    @classmethod
    def from_env(cls) -> "KafkaSettings":
        bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

        return cls(
            bootstrap_servers=bootstrap_servers.split(","),
            topics_prefix=os.getenv("KAFKA_TOPICS_PREFIX", "yurest"),
            consumer_group_id=os.getenv("KAFKA_CONSUMER_GROUP_ID", "yurest-app"),
            enable_auto_commit=os.getenv("KAFKA_ENABLE_AUTO_COMMIT", "true").lower()
            == "true",
            auto_offset_reset=os.getenv("KAFKA_AUTO_OFFSET_RESET", "earliest"),
            max_poll_records=int(os.getenv("KAFKA_MAX_POLL_RECORDS", "500")),
            session_timeout_ms=int(os.getenv("KAFKA_SESSION_TIMEOUT_MS", "30000")),
            heartbeat_interval_ms=int(os.getenv("KAFKA_HEARTBEAT_INTERVAL_MS", "3000")),
            enabled=os.getenv("KAFKA_ENABLED", "true").lower() == "true",
        )

    def get_topic_name(self, event_name: str) -> str:
        """Genera el nombre del topic basado en el prefijo y el nombre del evento"""
        return f"{self.topics_prefix}.{event_name.replace('.', '_')}"
