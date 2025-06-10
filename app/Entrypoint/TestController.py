import logging

from fastapi import APIRouter, Response

from app.Contexts.Shared.Infrastructure.Http.Context.RequestContext import (
    RequestContext,
)
from app.Contexts.Shared.Infrastructure.Http.Controller import Controller


class TestController(Controller):
    _logger: logging.Logger = logging.getLogger(__name__)

    def get_router(self) -> APIRouter:
        router = APIRouter()
        router.add_api_route("/test", self.get_test_route, methods=["GET"])
        return router

    def get_test_route(self) -> Response:
        # Ejemplo de uso del contexto
        trace_id = RequestContext.get_trace_id()
        client_ip = RequestContext.get_client_ip()

        # Log simple - el trace_id se incluye automáticamente
        self._logger.info(f"Processing test request from {client_ip}")

        return Response(
            content=f"Hello, World! Trace ID: {trace_id}",
            headers={"Content-Type": "text/plain"},
        )
