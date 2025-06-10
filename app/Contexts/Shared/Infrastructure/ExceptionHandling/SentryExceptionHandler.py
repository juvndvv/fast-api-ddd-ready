import logging
from typing import override

from fastapi import Request
from starlette.responses import JSONResponse

from app.Contexts.Shared.Domain.ExceptionHandling.ExceptionHandler import (
    ExceptionHandler,
)


class SentryExceptionHandler(ExceptionHandler):
    _logger: logging.Logger = logging.getLogger(__name__)

    @override
    async def handle(self, request: Request, exc: Exception) -> JSONResponse:
        self._logger.info(f"Error occurred: {str(exc)}", exc_info=exc)

        # TODO: Integrar Sentry

        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "message": str(exc)},
        )
