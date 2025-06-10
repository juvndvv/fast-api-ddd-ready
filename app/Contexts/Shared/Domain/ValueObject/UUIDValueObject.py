from uuid import UUID, uuid4

from app.Contexts.Shared.Domain.ValueObject.ValueObject import ValueObject

# El método `value()` devolverá la representación en cadena del UUID.


class UUIDValueObject(ValueObject[str]):
    """
    Base class for UUID-based Value Objects.
    Handles unique identifiers in the domain using UUID v4 (random).
    """

    __slots__ = ("_value",)

    def __init__(self, value: UUID | str | None = None):
        if value is None:
            self._value = uuid4()
        elif isinstance(value, str):
            try:
                self._value = UUID(value)
            except ValueError as e:
                raise ValueError("Invalid UUID format") from e
        elif isinstance(value, UUID):
            self._value = value
        else:
            raise ValueError("Value must be a UUID, string or None")

    def value(self) -> str:  # noqa: D401
        return str(self._value)

    @classmethod
    def generate(cls) -> "UUIDValueObject":
        """
        Generates a new UUID v4 Value Object.
        """
        return cls(None)
