import logging
import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response

from app.Contexts.Shared.Infrastructure.Http.Middleware.Middleware import Middleware


class LoggingMiddleware(Middleware):
    _logger: logging.Logger = logging.getLogger(__name__)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        method = request.method
        url = str(request.url)
        client_host = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")

        self._logger.info(
            f"Request started: {method} {url} from {client_host} ({user_agent})"
        )

        start_time = time.time()

        try:
            response = await call_next(request)

            process_time = time.time() - start_time

            self._logger.info(
                f"Request completed: {method} {url} - Status: {response.status_code} - Time: {process_time:.2f}s"
            )

            return response

        except Exception as e:
            process_time = time.time() - start_time

            self._logger.error(
                f"Request failed: {method} {url} - Error: {str(e)} - Time: {process_time:.2f}s",
                exc_info=e,
            )
            raise
