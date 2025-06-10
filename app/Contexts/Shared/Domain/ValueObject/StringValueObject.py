import re
from typing import ClassVar

from app.Contexts.Shared.Domain.ValueObject.ValueObject import ValueObject


class StringValueObject(ValueObject[str]):
    """
    Value Object base para cadenas de texto.
    Permite validaciones opcionales de longitud y expresión regular.
    """

    # Validaciones configurables por subclase --------------------------------------------------
    MIN_LENGTH: ClassVar[int | None] = None
    MAX_LENGTH: ClassVar[int | None] = None
    REGEX_PATTERN: ClassVar[str | None] = None

    __slots__ = ("_value",)

    def __init__(self, value: str):
        self._value = value
        self._ensure_is_valid()

    # Validaciones ---------------------------------------------------------------------------

    def _ensure_is_valid(self) -> None:
        if not isinstance(self._value, str):
            raise ValueError(f"Value {self._value!r} is not a valid string")

        if self.MIN_LENGTH is not None and len(self._value) < self.MIN_LENGTH:
            raise ValueError(f"String shorter than minimum length {self.MIN_LENGTH}")

        if self.MAX_LENGTH is not None and len(self._value) > self.MAX_LENGTH:
            raise ValueError(f"String longer than maximum length {self.MAX_LENGTH}")

        if self.REGEX_PATTERN is not None and not re.match(
            self.REGEX_PATTERN, self._value
        ):
            raise ValueError("String does not match required pattern")

    # API pública -----------------------------------------------------------------------------

    def value(self) -> str:  # noqa: D401 (getter should be method)
        return self._value

    # Python dunder methods -------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:  # type: ignore[override]
        if not isinstance(other, StringValueObject):
            return False
        return self._value == other._value

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._value})"
