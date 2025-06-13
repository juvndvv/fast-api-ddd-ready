from app.Contexts.Shared.Application.Bus.Query.Query import Query


class PaginateMessagesQuery(Query):
    """Query para paginar mensajes de una conversación con cursor"""

    MAX_LIMIT = 100
    DEFAULT_LIMIT = 20

    def __init__(
        self, conversation_id: str, cursor: str | None = None, limit: int | None = None
    ) -> None:
        self.conversation_id = conversation_id
        self.cursor = cursor
        # Aplicar límite máximo de seguridad
        if limit is None:
            self.limit = self.DEFAULT_LIMIT
        else:
            self.limit = min(limit, self.MAX_LIMIT)
