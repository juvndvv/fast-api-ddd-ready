from numbers import Number
from typing import Any, TypeVar, cast, override

from app.Contexts.Shared.Domain.ValueObject.ValueObject import ValueObject

T = TypeVar("T", bound=int | float)


class NumericValueObject(ValueObject[T]):
    """
    Base class for numeric-based Value Objects.
    Implements comparison magic methods for numeric operations.
    """

    __slots__ = ("_value",)

    def __init__(self, value: T):
        if not isinstance(value, Number):
            raise ValueError("Value must be a number")
        self._value: T = value

    @override
    def value(self) -> T:
        return self._value

    def __lt__(self, other: "NumericValueObject[T] | T") -> bool:
        """
        Less than comparison.
        """
        if isinstance(other, NumericValueObject):
            return bool(cast(Any, self._value) < cast(Any, other.value()))
        return bool(cast(Any, self._value) < other)

    def __le__(self, other: "NumericValueObject[T] | T") -> bool:
        """
        Less than or equal comparison.
        """
        if isinstance(other, NumericValueObject):
            return bool(cast(Any, self._value) <= cast(Any, other.value()))
        return bool(cast(Any, self._value) <= other)

    def __eq__(self, other: "NumericValueObject[T] | T") -> bool:
        """
        Equal comparison.
        """
        if isinstance(other, NumericValueObject):
            return self._value == other.value()
        return self._value == other

    def __ne__(self, other: "NumericValueObject[T] | T") -> bool:
        """
        Not equal comparison.
        """
        if isinstance(other, NumericValueObject):
            return self._value != other.value()
        return self._value != other

    def __gt__(self, other: "NumericValueObject[T] | T") -> bool:
        """
        Greater than comparison.
        """
        if isinstance(other, NumericValueObject):
            return bool(cast(Any, self._value) > cast(Any, other.value()))
        return bool(cast(Any, self._value) > other)

    def __ge__(self, other: "NumericValueObject[T] | T") -> bool:
        """
        Greater than or equal comparison.
        """
        if isinstance(other, NumericValueObject):
            return bool(cast(Any, self._value) >= cast(Any, other.value()))
        return bool(cast(Any, self._value) >= other)

    def __add__(self, other: "NumericValueObject[T] | T") -> T:
        """
        Addition operation.
        """
        if isinstance(other, NumericValueObject):
            return cast(T, cast(Any, self._value) + cast(Any, other.value()))
        return cast(T, cast(Any, self._value) + other)

    def __sub__(self, other: "NumericValueObject[T] | T") -> T:
        """
        Subtraction operation.
        """
        if isinstance(other, NumericValueObject):
            return cast(T, cast(Any, self._value) - cast(Any, other.value()))
        return cast(T, cast(Any, self._value) - other)

    def __mul__(self, other: "NumericValueObject[T] | T") -> T:
        """
        Multiplication operation.
        """
        if isinstance(other, NumericValueObject):
            return cast(T, cast(Any, self._value) * cast(Any, other.value()))
        return cast(T, cast(Any, self._value) * other)

    def __truediv__(self, other: "NumericValueObject[T] | T") -> T:
        """
        True division operation.
        """
        if isinstance(other, NumericValueObject):
            return cast(T, cast(Any, self._value) / cast(Any, other.value()))
        return cast(T, cast(Any, self._value) / other)

    def __floordiv__(self, other: "NumericValueObject[T] | T") -> T:
        """
        Floor division operation.
        """
        if isinstance(other, NumericValueObject):
            return cast(T, cast(Any, self._value) // cast(Any, other.value()))
        return cast(T, cast(Any, self._value) // other)

    def __mod__(self, other: "NumericValueObject[T] | T") -> T:
        """
        Modulo operation.
        """
        if isinstance(other, NumericValueObject):
            return cast(T, cast(Any, self._value) % cast(Any, other.value()))
        return cast(T, cast(Any, self._value) % other)

    def __pow__(self, other: "NumericValueObject[T] | T") -> T:
        """
        Power operation.
        """
        if isinstance(other, NumericValueObject):
            return cast(T, cast(Any, self._value) ** cast(Any, other.value()))
        return cast(T, cast(Any, self._value) ** other)
