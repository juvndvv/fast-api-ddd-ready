from typing import override

from app.Contexts.Shared.Domain.ValueObject.NumericValueObject import NumericValueObject


class IntegerValueObject(NumericValueObject[int]):
    """
    Base class for integer-based Value Objects.
    """

    def __init__(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Value must be an integer")
        super().__init__(value)

    @override
    def value(self) -> int:
        return self._value
