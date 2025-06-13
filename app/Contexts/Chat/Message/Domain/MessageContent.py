from __future__ import annotations


class MessageContent:
    """Value Object para contenido de mensaje"""

    def __init__(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("MessageContent no puede estar vacío")
        if len(value.strip()) > 1000:
            raise ValueError("MessageContent no puede superar 1000 caracteres")
        self._value = value.strip()

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, MessageContent) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"MessageContent({self._value!r})"
