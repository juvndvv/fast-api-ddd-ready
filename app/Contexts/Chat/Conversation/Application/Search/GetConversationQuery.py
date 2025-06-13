from app.Contexts.Shared.Application.Bus.Query.Query import Query


class GetConversationQuery(Query):
    """Query para obtener metadatos de una conversación sin mensajes"""

    def __init__(self, conversation_id: str) -> None:
        self.conversation_id = conversation_id
