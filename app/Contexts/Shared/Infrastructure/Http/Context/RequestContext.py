from app.Contexts.Shared.Infrastructure.Http.Middleware.RequestContextMiddleware import (
    request_context,
)


class RequestContext:
    """Utilidad para acceder al contexto del request actual."""

    @staticmethod
    def get_trace_id() -> str | None:
        """Obtiene el trace_id del request actual."""
        context = request_context.get({})
        return context.get("trace_id")

    @staticmethod
    def get_context() -> dict[str, str]:
        """Obtiene todo el contexto del request actual."""
        return request_context.get({})

    @staticmethod
    def get_client_ip() -> str | None:
        """Obtiene la IP del cliente del request actual."""
        context = request_context.get({})
        return context.get("client_ip")

    @staticmethod
    def get_method() -> str | None:
        """Obtiene el método HTTP del request actual."""
        context = request_context.get({})
        return context.get("method")

    @staticmethod
    def get_url() -> str | None:
        """Obtiene la URL del request actual."""
        context = request_context.get({})
        return context.get("url")
