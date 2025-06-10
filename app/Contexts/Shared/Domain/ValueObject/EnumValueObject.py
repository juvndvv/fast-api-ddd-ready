from enum import Enum
from typing import Generic, TypeVar

from app.Contexts.Shared.Domain.ValueObject.ValueObject import ValueObject

T = TypeVar("T", bound=Enum)


class EnumValueObject(ValueObject[str], Generic[T]):
    """
    Base class for Enum Value Objects.
    """

    def __init__(self, value: T):
        self._value = value
        self.ensure_is_valid()

    def ensure_is_valid(self) -> None:
        """
        Ensures that the value is valid.
        """
        if not isinstance(self._value, Enum):
            raise ValueError(f"Value {self._value} is not a valid Enum")

    @property
    def value(self) -> str:
        """
        Returns the value as string.

        Returns:
            str: El valor como string.
        """
        return str(self._value.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EnumValueObject):
            return False
        return bool(self._value == other._value)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"
