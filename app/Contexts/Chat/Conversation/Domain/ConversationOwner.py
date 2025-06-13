from __future__ import annotations


class ConversationOwner:
    """Value Object para propietario de conversación"""

    def __init__(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("ConversationOwner no puede estar vacío")
        self._value = value.strip()

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ConversationOwner) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"ConversationOwner({self._value!r})"
