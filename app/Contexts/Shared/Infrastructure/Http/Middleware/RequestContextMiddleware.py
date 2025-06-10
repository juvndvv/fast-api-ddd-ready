import logging
import uuid
from collections.abc import Awaitable, Callable
from contextvars import ContextVar

from fastapi import Request, Response

from app.Contexts.Shared.Infrastructure.Http.Middleware.Middleware import Middleware

# Context variables para el request
request_context: ContextVar[dict[str, str]] = ContextVar(
    "request_context", default={}  # noqa: B039
)


class RequestContextMiddleware(Middleware):
    _logger: logging.Logger = logging.getLogger(__name__)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Generar trace_id único para este request
        trace_id = str(uuid.uuid4())

        # Obtener trace_id del header si existe (para requests encadenados)
        if "X-Trace-ID" in request.headers:
            trace_id = request.headers["X-Trace-ID"]

        # Inicializar contexto del request
        context = {
            "trace_id": trace_id,
            "method": request.method,
            "url": str(request.url),
            "client_ip": request.client.host if request.client else "unknown",
        }

        # Establecer el contexto para este request
        token = request_context.set(context)

        try:
            self._logger.info(f"Request started: {request.method} {request.url}")

            # Continuar con el siguiente middleware/handler
            response = await call_next(request)

            # Agregar trace_id al header de respuesta
            response.headers["X-Trace-ID"] = trace_id

            self._logger.info(f"Request completed: Status {response.status_code}")

            return response

        except Exception as e:
            self._logger.error(f"Request failed: {str(e)}", exc_info=e)
            raise
        finally:
            # Limpiar el contexto
            request_context.reset(token)
