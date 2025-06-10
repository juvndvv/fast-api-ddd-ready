from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, override

T = TypeVar("T")


class ValueObject(ABC, Generic[T]):
    """
    Abstract base class for Value Objects in the domain.
    Value Objects are immutable objects that are defined by their attributes.

    Type Parameters:
        T: The type of value that this Value Object represents.
    """

    __slots__ = ()  # Avoid instance __dict__ by default, subclasses must declare their own slots

    @abstractmethod
    def value(self) -> T:
        """
        Returns the value of the Value Object.
        """
        raise NotImplementedError

    @override
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.value()})"

    def __repr__(self) -> str:  # pragma: no cover
        return str(self)

    def __eq__(self, other: Any) -> bool:
        """
        Compares if two Value Objects are equal based on their attributes.
        """
        if not isinstance(other, self.__class__):
            return False
        return self.value() == other.value()

    def __hash__(self) -> int:
        """
        Generates a hash based on the Value Object's attributes.
        """
        return hash((self.__class__, self.value()))

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the Value Object to a dictionary.
        """
        return {"value": self.value()}
