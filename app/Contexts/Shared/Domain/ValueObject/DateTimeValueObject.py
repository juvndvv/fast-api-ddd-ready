from __future__ import annotations

from datetime import UTC, datetime
from typing import ClassVar, override

from app.Contexts.Shared.Domain.ValueObject.ValueObject import ValueObject


class DateTimeValueObject(ValueObject[datetime]):
    """Value Object para instantes de tiempo (aware)."""

    __slots__ = ("_value",)

    _FORMAT: ClassVar[str] = "%Y-%m-%dT%H:%M:%S%z"

    # ---------------------------------------------------------------------
    # Constructor y validación
    # ---------------------------------------------------------------------

    def __init__(self, value: datetime):
        if not isinstance(value, datetime):
            raise ValueError("Value must be a datetime object")
        # Normalizamos a timezone-aware UTC para coherencia interna
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        self._value = value

    # ---------------------------------------------------------------------
    # API pública
    # ---------------------------------------------------------------------

    @override
    def value(self) -> datetime:
        return self._value

    # Factory methods ------------------------------------------------------

    @classmethod
    def now(cls) -> DateTimeValueObject:
        """Crea un VO con el instante actual en UTC."""
        return cls(datetime.now(tz=UTC))

    @classmethod
    def from_iso_string(cls, iso_str: str) -> DateTimeValueObject:
        """Construye el VO a partir de una cadena ISO 8601."""
        try:
            dt = datetime.fromisoformat(iso_str)
        except ValueError as e:
            raise ValueError("Invalid ISO datetime format") from e
        return cls(dt)

    # Conversion helpers ---------------------------------------------------

    def to_iso_string(self) -> str:
        return self._value.isoformat()

    def to_utc_iso_string(self) -> str:
        return self._value.astimezone(UTC).isoformat()

    def to_date_string(self) -> str:
        return self._value.date().isoformat()

    def to_time_string(self) -> str:
        return self._value.time().isoformat()

    # Comparación ----------------------------------------------------------

    def __lt__(self, other: DateTimeValueObject | datetime) -> bool:
        other_dt = other.value() if isinstance(other, DateTimeValueObject) else other
        return self._value < other_dt

    def __le__(self, other: DateTimeValueObject | datetime) -> bool:  # type: ignore[override]
        other_dt = other.value() if isinstance(other, DateTimeValueObject) else other
        return self._value <= other_dt

    def __gt__(self, other: DateTimeValueObject | datetime) -> bool:  # type: ignore[override]
        other_dt = other.value() if isinstance(other, DateTimeValueObject) else other
        return self._value > other_dt

    def __ge__(self, other: DateTimeValueObject | datetime) -> bool:  # type: ignore[override]
        other_dt = other.value() if isinstance(other, DateTimeValueObject) else other
        return self._value >= other_dt

    # Semánticos -----------------------------------------------------------

    def is_before(self, other: DateTimeValueObject) -> bool:
        return self._value < other.value()

    def is_after(self, other: DateTimeValueObject) -> bool:
        return self._value > other.value()

    def is_same(self, other: DateTimeValueObject) -> bool:
        return self._value == other.value()
