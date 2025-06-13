"""
Chat Module for registering commands, queries, events and providing dependencies.
"""

from typing import Any

from injector import Binder, Module, singleton

from app.Contexts.Chat.Conversation.Application.Search.GetConversationQuery import (
    GetConversationQuery,
)
from app.Contexts.Chat.Conversation.Application.Search.GetConversationQueryHandler import (
    GetConversationQueryHandler,
)
from app.Contexts.Chat.Conversation.Infrastructure.Http.GetConversationController import (
    GetConversationController,
)
from app.Contexts.Chat.Conversation.Infrastructure.Repository.ConversationRepository import (
    ConversationRepository,
)
from app.Contexts.Chat.Infrastructure.Repository.InMemoryConversationRepository import (
    InMemoryConversationRepository,
)
from app.Contexts.Chat.Infrastructure.Repository.InMemoryMessageRepository import (
    InMemoryMessageRepository,
)
from app.Contexts.Chat.Message.Application.Create.UpsertMessageCommand import (
    UpsertMessageCommand,
)
from app.Contexts.Chat.Message.Application.Create.UpsertMessageCommandHandler import (
    UpsertMessageCommandHandler,
)
from app.Contexts.Chat.Message.Application.Search.PaginateMessagesQuery import (
    PaginateMessagesQuery,
)
from app.Contexts.Chat.Message.Application.Search.PaginateMessagesQueryHandler import (
    PaginateMessagesQueryHandler,
)
from app.Contexts.Chat.Message.Domain.MessageChronologyChecker import (
    MessageChronologyChecker,
)
from app.Contexts.Chat.Message.Infrastructure.Http.PaginateMessagesController import (
    PaginateMessagesController,
)
from app.Contexts.Chat.Message.Infrastructure.Http.UpsertMessageController import (
    UpsertMessageController,
)
from app.Contexts.Chat.Message.Infrastructure.Repository.MessageRepository import (
    MessageRepository,
)
from app.Contexts.Shared.Infrastructure.Module.ApplicationModule import (
    ApplicationModule,
)


class ChatModule(ApplicationModule, Module):
    """Module for Chat bounded context dependencies and registrations"""

    def configure(self, binder: Binder) -> None:
        """Configure dependency injection bindings"""
        # For testing purposes, we use mocks for repositories
        # In a real implementation, these would bind to actual implementations

        # Repository implementations - singleton for state persistence in tests
        binder.bind(
            ConversationRepository, to=InMemoryConversationRepository, scope=singleton
        )  # type: ignore
        binder.bind(MessageRepository, to=InMemoryMessageRepository, scope=singleton)  # type: ignore

        # Domain services
        binder.bind(MessageChronologyChecker, scope=singleton)

        # Command handlers
        binder.bind(UpsertMessageCommandHandler, scope=singleton)

        # Query handlers
        binder.bind(GetConversationQueryHandler, scope=singleton)
        binder.bind(PaginateMessagesQueryHandler, scope=singleton)

        # Controllers
        binder.bind(UpsertMessageController, scope=singleton)
        binder.bind(GetConversationController, scope=singleton)
        binder.bind(PaginateMessagesController, scope=singleton)

    def map_commands(self) -> list[tuple[type[Any], type[Any]]]:
        """Map commands to their handlers"""
        return [
            (UpsertMessageCommand, UpsertMessageCommandHandler),
        ]

    def map_queries(self) -> list[tuple[type[Any], type[Any]]]:
        """Map queries to their handlers"""
        return [
            (GetConversationQuery, GetConversationQueryHandler),
            (PaginateMessagesQuery, PaginateMessagesQueryHandler),
        ]

    def map_events(self) -> list[tuple[type[Any], type[Any]]]:
        """Map events to their listeners"""
        # No event listeners implemented yet
        return []
