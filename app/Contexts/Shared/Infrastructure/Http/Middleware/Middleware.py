from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware


class Middleware(ABC, BaseHTTPMiddleware):
    def __init__(self, app: Starlette):
        super().__init__(app)

    @abstractmethod
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Método que debe ser implementado por los middlewares concretos.
        Args:
            request: La petición HTTP
            call_next: Función para continuar con el siguiente middleware
        Returns:
            Response: La respuesta HTTP
        """
        pass
