import logging

from injector import inject, singleton

from app.Contexts.Shared.Application.Bus.Event.EventBus import EventBus
from app.Contexts.Shared.Domain.DomainEvent import DomainEvent
from app.Contexts.Shared.Infrastructure.Settings.KafkaSettings import KafkaSettings


@singleton
class KafkaEventBusManager:
    """Manager para gestionar el ciclo de vida del EventBus de Kafka"""

    _logger: logging.Logger = logging.getLogger(__name__)

    @inject
    def __init__(self, event_bus: EventBus, kafka_settings: KafkaSettings) -> None:
        self._event_bus = event_bus
        self._kafka_settings = kafka_settings
        self._started = False

        # Debug: agregar identificador de instancia
        self._instance_id = str(id(self._event_bus))
        self._logger.info(
            f"KafkaEventBusManager creado con EventBus instancia: {self._instance_id}"
        )

    async def start(self) -> None:
        """Inicia el EventBus de Kafka"""
        if not self._kafka_settings.enabled:
            self._logger.info("Kafka deshabilitado por configuración")
            return

        if not self._started:
            await self._event_bus.start()
            self._started = True
            self._logger.info("KafkaEventBusManager iniciado")

    async def stop(self) -> None:
        """Detiene el EventBus de Kafka"""
        if not self._kafka_settings.enabled:
            return

        if self._started:
            await self._event_bus.stop()
            self._started = False
            self._logger.info("KafkaEventBusManager detenido")

    async def publish_events(self, events: list[DomainEvent]) -> None:
        """Publica eventos de dominio"""
        if not self._kafka_settings.enabled:
            self._logger.debug("Kafka deshabilitado, eventos no publicados")
            return

        if not self._started:
            self._logger.warning("EventBus no iniciado, iniciando automáticamente...")
            await self.start()

        await self._event_bus.publish(events)
