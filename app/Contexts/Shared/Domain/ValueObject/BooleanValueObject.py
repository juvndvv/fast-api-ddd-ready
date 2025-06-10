from typing import override

from app.Contexts.Shared.Domain.ValueObject.ValueObject import ValueObject


class BooleanValueObject(ValueObject[bool]):
    """
    Base class for boolean-based Value Objects.
    """

    def __init__(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("Value must be a boolean")
        self._value = value

    @override
    def value(self) -> bool:
        return self._value

    def __bool__(self) -> bool:
        """
        Allows direct boolean comparison of the Value Object.
        Example:
            if boolean_vo:  # Will use the internal value
                do_something()
        """
        return self._value
