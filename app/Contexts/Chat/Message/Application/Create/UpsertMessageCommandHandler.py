from app.Contexts.Chat.Conversation.Domain.Conversation import Conversation
from app.Contexts.Chat.Conversation.Domain.ConversationId import ConversationId
from app.Contexts.Chat.Conversation.Domain.ConversationOwner import ConversationOwner
from app.Contexts.Chat.Conversation.Domain.ConversationTruncatedEvent import (
    ConversationTruncatedEvent,
)
from app.Contexts.Chat.Conversation.Infrastructure.Repository.ConversationRepository import (
    ConversationRepository,
)
from app.Contexts.Chat.Message.Application.Create.UpsertMessageCommand import (
    UpsertMessageCommand,
)
from app.Contexts.Chat.Message.Domain.Message import Message
from app.Contexts.Chat.Message.Domain.MessageChronologyChecker import (
    MessageChronologyChecker,
)
from app.Contexts.Chat.Message.Domain.MessageContent import MessageContent
from app.Contexts.Chat.Message.Domain.MessageId import MessageId
from app.Contexts.Chat.Message.Infrastructure.Repository.MessageRepository import (
    MessageRepository,
)
from app.Contexts.Shared.Application.Bus.Command.CommandHandler import CommandHandler
from app.Contexts.Shared.Application.Bus.Event.EventBus import EventBus
from app.Contexts.Shared.Domain.AggregateRoot import AggregateRoot


class UpsertMessageCommandHandler(CommandHandler):
    """Handler para el comando UpsertMessage que implementa la lógica de negocio atómica"""

    def __init__(
        self,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository,
        chronology_checker: MessageChronologyChecker,
        event_bus: EventBus,
    ) -> None:
        self._conversation_repository = conversation_repository
        self._message_repository = message_repository
        self._chronology_checker = chronology_checker
        self._event_bus = event_bus

    async def handle(self, command: UpsertMessageCommand) -> None:
        """
        Maneja el comando UpsertMessage implementando:
        1. Creación de conversación si no existe
        2. Creación o actualización de mensaje
        3. Eliminación de mensajes posteriores si es actualización
        4. Publicación de eventos de dominio
        """
        conversation_id = ConversationId(command.conversation_id)
        message_id = MessageId(command.message_id)
        content = MessageContent(command.content)
        owner = ConversationOwner(command.owner)

        # 1. Obtener o crear conversación
        conversation = self._get_or_create_conversation(conversation_id, owner)

        # 2. Obtener mensaje existente si existe
        existing_message = self._message_repository.find_by_id(message_id)

        # 3. Validar consistencia de IDs si el mensaje existe
        if existing_message and existing_message.id != message_id:
            raise ValueError(
                "Message ID inmutable: no se puede cambiar el ID del mensaje"
            )

        # 4. Crear o actualizar mensaje
        if existing_message:
            # Actualizar mensaje existente
            existing_message.update_content(content)
            message = existing_message

            # Obtener mensajes posteriores para eliminar
            posterior_messages = self._chronology_checker.get_messages_after(
                conversation_id, message_id
            )
            if posterior_messages:
                # Soft delete de mensajes posteriores
                self._message_repository.soft_delete_messages(posterior_messages)
                # Publicar evento de truncamiento
                conversation._record(
                    ConversationTruncatedEvent(str(conversation_id), str(message_id))
                )
        else:
            # Crear nuevo mensaje
            message = Message.create(message_id, conversation_id, content)

        # 5. Actualizar última mensaje de la conversación
        conversation.update_last_message(message_id)

        # 6. Persistir cambios
        self._conversation_repository.save(conversation)
        self._message_repository.save(message)

        # 7. Publicar eventos de dominio
        await self._publish_events(conversation)
        await self._publish_events(message)

    def _get_or_create_conversation(
        self, conversation_id: ConversationId, owner: ConversationOwner
    ) -> Conversation:
        """Obtiene una conversación existente o crea una nueva"""
        existing_conversation = self._conversation_repository.find_by_id(
            conversation_id
        )
        if existing_conversation:
            return existing_conversation

        return Conversation.create(conversation_id, owner)

    async def _publish_events(self, aggregate: AggregateRoot) -> None:
        """Publica los eventos de dominio de un agregado"""
        events = aggregate.pull_domain_events()
        if events:
            await self._event_bus.publish(events)
