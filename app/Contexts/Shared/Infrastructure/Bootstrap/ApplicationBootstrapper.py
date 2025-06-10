import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from injector import Injector, Module

from app.Contexts.Shared.Application.Bus.Command.CommandBus import CommandBus
from app.Contexts.Shared.Application.Bus.Event.EventBus import EventBus
from app.Contexts.Shared.Application.Bus.Query.QueryBus import QueryBus
from app.Contexts.Shared.Domain.ExceptionHandling.ExceptionHandler import (
    ExceptionHandler,
)
from app.Contexts.Shared.Infrastructure.Bootstrap.ClassFinder import ClassFinder
from app.Contexts.Shared.Infrastructure.Bus.Event.KafkaEventBusManager import (
    KafkaEventBusManager,
)
from app.Contexts.Shared.Infrastructure.Http.Controller import Controller
from app.Contexts.Shared.Infrastructure.Http.Middleware.Middleware import Middleware
from app.Contexts.Shared.Infrastructure.Logging.LoggerConfig import configure_logging
from app.Contexts.Shared.Infrastructure.Module.ApplicationModule import (
    ApplicationModule,
)

# Configurar logging al inicio
configure_logging()


class ApplicationBootstrapper:
    _logger: logging.Logger = logging.getLogger(__name__)
    _modules: list[type[ApplicationModule]] | None = None
    _app: FastAPI | None = None
    _injector: Injector | None = None
    _initialized: bool = False

    def __init__(self) -> None:
        if not self._initialized:
            self._modules = ClassFinder.find(Module, "Module")  # type: ignore[arg-type]
            self._initialize_injector()
            self._initialize_app()
            self._initialize_commands()
            self._initialize_queries()
            self._initialize_events()
            self._initialized = True

    def _initialize_injector(self) -> None:
        if not self._injector:
            self._logger.info("Initializing container")
            self._injector = Injector(modules=self._modules)

    def _initialize_commands(self) -> None:
        self._logger.info("Initializing commands")

        if not self._injector or not self._modules:
            raise RuntimeError("Injector or modules not initialized")

        bus = self._injector.get(CommandBus)  # type: ignore

        for module_class in self._modules:
            module: ApplicationModule = self._injector.get(module_class)  # type: ignore
            for command, handler in module.map_commands():
                bus.register(command, handler)

    def _initialize_queries(self) -> None:
        self._logger.info("Initializing queries")

        if not self._injector or not self._modules:
            raise RuntimeError("Injector or modules not initialized")

        bus = self._injector.get(QueryBus)  # type: ignore

        for module_class in self._modules:
            module: ApplicationModule = self._injector.get(module_class)  # type: ignore
            for query, handler in module.map_queries():
                bus.register(query, handler)

    def _initialize_events(self) -> None:
        self._logger.info("Initializing events")

        if not self._injector or not self._modules:
            raise RuntimeError("Injector or modules not initialized")

        event_bus = self._injector.get(EventBus)  # type: ignore

        for module_class in self._modules:
            module: ApplicationModule = self._injector.get(module_class)  # type: ignore
            for event, listener in module.map_events():
                event_bus.register(event, listener)

    def _initialize_app(self) -> None:
        if not self._app:
            self._app = FastAPI(
                title="Yurest AI API",
                description="API para el sistema de IA de Yurest",
                version="1.0.0",
                docs_url="/docs",
                redoc_url="/redoc",
                openapi_url="/openapi.json",
                lifespan=self._lifespan,
            )

            # Inicializar middlewares
            self._logger.info("Initializing middlewares")
            middlewares = ClassFinder.find(Middleware, "Middleware")  # type: ignore
            for middleware_class in middlewares:
                self._app.add_middleware(middleware_class)  # type: ignore

    @asynccontextmanager
    async def _lifespan(self, app: FastAPI) -> AsyncGenerator[None]:
        # Startup
        await self.start_application()

        # Inicializar EventBus de Kafka después de que todo esté configurado
        self._logger.info("Initializing Kafka EventBus")
        kafka_manager = self._injector.get(KafkaEventBusManager)  # type: ignore
        await kafka_manager.start()

        yield

        # Shutdown
        self._logger.info("Shutting down application")
        kafka_manager = self._injector.get(KafkaEventBusManager)  # type: ignore
        await kafka_manager.stop()

    async def start_application(self) -> None:
        self._logger.info("Initializing FastAPI app")

        # Initialize exception handler
        self._logger.info("Initializing exception handler")
        exception_handlers = ClassFinder.find(ExceptionHandler, "ExceptionHandler")  # type: ignore
        if not exception_handlers:
            self._logger.error("No exception handler implementation found")
            raise RuntimeError("No exception handler implementation found")
        exception_handler_class = exception_handlers[0]
        exception_handler = self._injector.get(exception_handler_class)  # type: ignore
        self._app.add_exception_handler(BaseException, exception_handler.handle)  # type: ignore

        # Initialize controllers
        self._logger.info("Initializing controllers")
        controllers = ClassFinder.find(Controller, "Controller")  # type: ignore
        for controller_class in controllers:
            controller = self._injector.get(controller_class)  # type: ignore

            if not isinstance(controller, Controller):
                continue

            self._app.include_router(controller.get_router())  # type: ignore

    @property
    def app(self) -> FastAPI:
        if not self._app:
            raise RuntimeError("FastAPI app not initialized")

        return self._app
