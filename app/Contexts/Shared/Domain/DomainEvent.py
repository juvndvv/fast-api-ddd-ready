from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from datetime import UTC, datetime
from typing import Any


class DomainEvent(ABC):
    __slots__ = ("_id", "_name", "_payload", "_occurred_on")

    def __init__(self, payload: dict[str, Any], occurred_on: datetime | None = None):
        self._id = str(uuid.uuid4())
        self._name = self.__class__.event_name()
        self._payload = payload
        self._occurred_on = occurred_on or datetime.now(tz=UTC)

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def payload(self) -> dict[str, Any]:
        return self._payload

    @property
    def occurred_on(self) -> datetime:
        return self._occurred_on

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DomainEvent) and self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    @classmethod
    @abstractmethod
    def event_name(cls) -> str: ...
