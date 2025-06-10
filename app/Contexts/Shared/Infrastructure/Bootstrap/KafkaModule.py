import logging

from injector import Binder, singleton

from app.Contexts.Shared.Application.Bus.Event.EventBus import EventBus
from app.Contexts.Shared.Infrastructure.Bus.Event.KafkaEventBus import KafkaEventBus
from app.Contexts.Shared.Infrastructure.Bus.Event.KafkaEventBusManager import (
    KafkaEventBusManager,
)
from app.Contexts.Shared.Infrastructure.Module.ApplicationModule import (
    ApplicationModule,
)
from app.Contexts.Shared.Infrastructure.Settings.KafkaSettings import KafkaSettings


class KafkaModule(ApplicationModule):
    _logger: logging.Logger = logging.getLogger(__name__)

    def configure(self, binder: Binder) -> None:
        self._logger.info("Configurando KafkaModule")
        super().configure(binder)

        # Configuración de Kafka
        binder.bind(KafkaSettings, to=KafkaSettings.from_env(), scope=singleton)

        # EventBus - registrar interfaz con implementación de Kafka
        binder.bind(EventBus, to=KafkaEventBus, scope=singleton)  # type: ignore

        # Registrar manager como singleton
        binder.bind(KafkaEventBusManager, scope=singleton)
