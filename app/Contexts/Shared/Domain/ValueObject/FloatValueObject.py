from typing import override

from app.Contexts.Shared.Domain.ValueObject.NumericValueObject import NumericValueObject


class FloatValueObject(NumericValueObject[float]):
    """
    Base class for float-based Value Objects.
    """

    def __init__(self, value: float) -> None:
        if not isinstance(value, int | float):
            raise ValueError("Value must be a number")
        super().__init__(float(value))

    @override
    def value(self) -> float:
        return self._value
