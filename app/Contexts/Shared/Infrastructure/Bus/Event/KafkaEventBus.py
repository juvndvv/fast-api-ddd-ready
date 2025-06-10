import asyncio
import logging
from typing import Any

import orjson
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from injector import Injector, inject, singleton

from app.Contexts.Shared.Application.Bus.Event.EventBus import EventBus
from app.Contexts.Shared.Application.Bus.Event.EventListener import EventListener
from app.Contexts.Shared.Domain.DomainEvent import DomainEvent
from app.Contexts.Shared.Infrastructure.Settings.KafkaSettings import KafkaSettings


@singleton
class KafkaEventBus(EventBus):
    _logger: logging.Logger = logging.getLogger(__name__)

    @inject
    def __init__(self, kafka_settings: KafkaSettings, injector: Injector) -> None:
        self._settings = kafka_settings
        self._injector = injector
        self._listeners: dict[str, list[type[EventListener]]] = {}
        self._subscriber_instances: dict[str, list[EventListener]] = {}
        self._producer: AIOKafkaProducer | None = None
        self._consumer: AIOKafkaConsumer | None = None
        self._consumer_task: asyncio.Task[None] | None = None
        self._is_running = False

        # Debug: agregar identificador de instancia
        self._instance_id = str(id(self))
        self._logger.info(f"Creada instancia de KafkaEventBus: {self._instance_id}")

    async def start(self) -> None:
        """Inicializa el producer y consumer de Kafka"""
        if self._is_running:
            self._logger.info(
                f"KafkaEventBus ya está ejecutándose (instancia {self._instance_id})"
            )
            return

        self._logger.info(f"Iniciando KafkaEventBus (instancia {self._instance_id})...")

        try:
            # Inicializar producer
            self._logger.info(
                f"Inicializando producer con bootstrap_servers: {self._settings.bootstrap_servers}"
            )
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self._settings.bootstrap_servers,
                value_serializer=self._serialize_event,
                key_serializer=lambda x: x.encode("utf-8") if x else None,
            )
            self._logger.info("Producer creado, iniciando conexión...")
            await self._producer.start()
            self._logger.info("Producer iniciado correctamente")

            # El consumer se iniciará de forma lazy cuando sea necesario
            self._logger.info(
                f"Estado de listeners: listeners={len(self._listeners)}, subscriber_instances={len(self._subscriber_instances)}"
            )
            self._logger.info(f"Listeners registrados: {list(self._listeners.keys())}")
            self._logger.info(
                f"Subscriber instances: {list(self._subscriber_instances.keys())}"
            )

            self._is_running = True

            # Inicializar consumer si hay listeners registrados
            if self._listeners or self._subscriber_instances:
                self._logger.info(
                    "Inicializando consumer porque hay listeners registrados..."
                )
                await self._ensure_consumer_started()

            self._logger.info("KafkaEventBus iniciado correctamente")

        except Exception as e:
            self._logger.error(f"Error iniciando KafkaEventBus: {e}")
            # Limpiar estado en caso de error
            if self._producer:
                try:
                    await self._producer.stop()
                except Exception:
                    pass
                self._producer = None
            raise

    async def stop(self) -> None:
        """Detiene el producer y consumer de Kafka"""
        if not self._is_running:
            return

        self._logger.info("Deteniendo KafkaEventBus...")
        self._is_running = False

        # Detener consumer
        if self._consumer_task:
            self._consumer_task.cancel()
            try:
                await self._consumer_task
            except asyncio.CancelledError:
                pass

        if self._consumer:
            await self._consumer.stop()

        # Detener producer
        if self._producer:
            await self._producer.stop()

        self._logger.info("KafkaEventBus detenido correctamente")

    async def publish(self, events: list[DomainEvent]) -> None:
        """Publica eventos a Kafka"""
        if not self._producer:
            self._logger.warning(
                "Producer no inicializado, no se pueden publicar eventos"
            )
            return

        self._logger.info(f"Publicando {len(events)} eventos a Kafka...")

        for event in events:
            event_name = event.__class__.__name__
            topic_name = self._settings.get_topic_name(event_name)

            try:
                self._logger.info(f"Enviando evento {event_name} a topic {topic_name}")
                await self._producer.send(
                    topic=topic_name,
                    value=event,
                    key=(
                        event.aggregate_id() if hasattr(event, "aggregate_id") else None
                    ),
                )
                self._logger.info(
                    f"Evento publicado exitosamente: {event_name} en topic {topic_name}"
                )

            except Exception as e:
                self._logger.error(f"Error publicando evento {event_name}: {e}")
                raise

    def register(self, event: type[DomainEvent], listener: type[EventListener]) -> None:
        """Registra un listener para un tipo de evento específico"""
        event_name = event.__name__

        if event_name not in self._listeners:
            self._listeners[event_name] = []

        self._listeners[event_name].append(listener)
        self._logger.info(
            f"Listener {listener.__name__} registrado para evento {event_name} (instancia {self._instance_id})"
        )

        # Inicializar consumer de forma lazy si es necesario
        if self._is_running:
            asyncio.create_task(self._ensure_consumer_started())

    def subscribe(self, event: type[DomainEvent], listener: EventListener) -> None:
        """Suscribe una instancia de listener para un tipo de evento específico"""
        event_name = event.__name__

        if event_name not in self._subscriber_instances:
            self._subscriber_instances[event_name] = []

        self._subscriber_instances[event_name].append(listener)
        self._logger.info(
            f"Listener instance {listener.__class__.__name__} suscrito para evento {event_name}"
        )

        # Inicializar consumer de forma lazy si es necesario
        if self._is_running:
            asyncio.create_task(self._ensure_consumer_started())

    async def _start_consumer(self) -> None:
        """Inicia el consumer de Kafka"""
        # Obtener todos los topics que necesitamos escuchar
        topics = [
            self._settings.get_topic_name(event_name)
            for event_name in set(
                list(self._listeners.keys()) + list(self._subscriber_instances.keys())
            )
        ]

        if not topics:
            return

        self._consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=self._settings.bootstrap_servers,
            group_id=self._settings.consumer_group_id,
            auto_offset_reset=self._settings.auto_offset_reset,
            enable_auto_commit=self._settings.enable_auto_commit,
            max_poll_records=self._settings.max_poll_records,
            session_timeout_ms=self._settings.session_timeout_ms,
            heartbeat_interval_ms=self._settings.heartbeat_interval_ms,
            value_deserializer=self._deserialize_event,
        )

        await self._consumer.start()
        self._consumer_task = asyncio.create_task(self._consume_events())
        self._logger.info(f"Consumer iniciado para topics: {topics}")

    async def _consume_events(self) -> None:
        """Consume eventos de Kafka y los procesa"""
        if not self._consumer:
            return

        try:
            async for message in self._consumer:
                try:
                    event_data = message.value
                    event_name = event_data.get("event_name")

                    self._logger.info(f"Mensaje recibido con event_name: {event_name}")

                    # Procesar listeners registrados (clases)
                    if event_name in self._listeners:
                        for listener_class in self._listeners[event_name]:
                            try:
                                # Crear instancia del listener usando el injector
                                listener_instance = self._injector.get(listener_class)  # type: ignore

                                # Reconstruir el evento desde los datos serializados
                                event = self._reconstruct_event(event_name, event_data)

                                self._logger.info(
                                    f"Ejecutando listener {listener_class.__name__} para evento {event_name}"
                                )
                                await listener_instance.listen(event)
                                self._logger.info(
                                    f"Listener {listener_class.__name__} ejecutado exitosamente"
                                )

                            except Exception as e:
                                self._logger.error(
                                    f"Error procesando evento {event_name} con listener {listener_class.__name__}: {e}"
                                )

                    # Procesar instancias de listeners suscritas
                    if event_name in self._subscriber_instances:
                        for listener_instance in self._subscriber_instances[event_name]:
                            try:
                                event = self._reconstruct_event(event_name, event_data)
                                self._logger.info(
                                    f"Ejecutando listener instance {listener_instance.__class__.__name__} para evento {event_name}"
                                )
                                await listener_instance.listen(event)
                                self._logger.info(
                                    f"Listener instance {listener_instance.__class__.__name__} ejecutado exitosamente"
                                )

                            except Exception as e:
                                self._logger.error(
                                    f"Error procesando evento {event_name} con listener instance {listener_instance.__class__.__name__}: {e}"
                                )

                    if (
                        event_name not in self._listeners
                        and event_name not in self._subscriber_instances
                    ):
                        self._logger.warning(
                            f"No hay listeners registrados para el evento: {event_name}"
                        )

                except Exception as e:
                    self._logger.error(f"Error procesando mensaje de Kafka: {e}")

        except asyncio.CancelledError:
            self._logger.info("Consumer cancelado")
        except Exception as e:
            self._logger.error(f"Error en consumer: {e}")

    def _reconstruct_event(
        self, event_name: str, event_data: dict[str, Any]
    ) -> DomainEvent:
        """Reconstruye un evento de dominio desde los datos serializados"""
        # Para simplificar, vamos a crear una instancia básica usando los datos del payload
        # En una implementación más robusta, esto podría usar un registry de eventos

        from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId
        from app.Contexts.Chat.Message.Domain.MessageCreatedEvent import (
            MessageCreatedEvent,
        )
        from app.Contexts.Chat.Message.Domain.MessageId import MessageId

        if event_name == "MessageCreatedEvent":
            payload = event_data.get("payload", {})
            message_id = MessageId(payload.get("message_id"))
            conversation_id = ConversationId(payload.get("conversation_id"))
            return MessageCreatedEvent(
                message_id=message_id, conversation_id=conversation_id
            )

        # Si no conocemos el evento, lanzar excepción
        raise ValueError(f"Tipo de evento desconocido: {event_name}")

    def _serialize_event(self, event: DomainEvent) -> bytes:
        """Serializa un evento de dominio a JSON"""
        try:
            event_data: dict[str, Any] = {
                "event_name": event.__class__.__name__,
                "aggregate_id": getattr(event, "aggregate_id", lambda: None)(),
                "occurred_on": event.occurred_on.isoformat(),
                "payload": event.payload,
            }
            return orjson.dumps(event_data)
        except Exception as e:
            self._logger.error(f"Error serializando evento: {e}")
            raise

    def _deserialize_event(self, data: bytes) -> dict[str, Any]:
        """Deserializa un evento de JSON"""
        try:
            result: dict[str, Any] = orjson.loads(data)
            return result
        except Exception as e:
            self._logger.error(f"Error deserializando evento: {e}")
            raise

    async def _ensure_consumer_started(self) -> None:
        """Asegura que el consumer esté iniciado (lazy initialization)"""
        if self._consumer is not None or not (
            self._listeners or self._subscriber_instances
        ):
            return

        self._logger.info("Iniciando consumer de forma lazy...")
        await self._start_consumer()
