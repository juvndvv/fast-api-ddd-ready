import logging
import sys
from logging import LogRecord

from colorama import Fore, Style, init

init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Formateador personalizado para logs con colores y trace_id."""

    COLORS = {
        "DEBUG": Fore.BLUE,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.RED + Style.BRIGHT,
    }

    def __init__(self, fmt: str | None = None, datefmt: str | None = None) -> None:
        super().__init__(fmt, datefmt)

    def format(self, record: LogRecord) -> str:
        """Formatea el registro de log con colores y trace_id."""
        # Obtener trace_id del contexto
        trace_id = self._get_trace_id()

        # Agregar trace_id al mensaje si existe
        if trace_id:
            if not record.getMessage().startswith(f"[{trace_id}]"):
                record.msg = f"[{trace_id}] {record.msg}"

        if not record.exc_info:
            levelname = record.levelname
            if levelname in self.COLORS:
                record.levelname = (
                    f"{self.COLORS[levelname]}{levelname}{Style.RESET_ALL}"
                )
        return super().format(record)

    def _get_trace_id(self) -> str | None:
        """Obtiene el trace_id del contexto actual."""
        try:
            from app.Contexts.Shared.Infrastructure.Http.Context.RequestContext import (
                RequestContext,
            )

            return RequestContext.get_trace_id()
        except Exception:
            # Si no se puede obtener el trace_id (fuera de contexto de request), retornar None
            return None


def configure_logging() -> None:
    """Configura el sistema de logging de la aplicación."""
    # Configurar el logger raíz
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Eliminar handlers existentes para evitar duplicación
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Crear y configurar el handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Crear el formateador con colores y trace_id
    formatter = ColoredFormatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    # Añadir el handler al logger raíz
    root_logger.addHandler(console_handler)

    # Configurar loggers específicos
    loggers = {
        "uvicorn": logging.INFO,
        "uvicorn.error": logging.INFO,
        "uvicorn.access": logging.WARNING,
        "fastapi": logging.INFO,
    }

    for logger_name, level in loggers.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        # Eliminar handlers existentes
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        # Añadir el handler de consola
        logger.addHandler(console_handler)
        # Evitar que los mensajes se propaguen al logger raíz
        logger.propagate = False
