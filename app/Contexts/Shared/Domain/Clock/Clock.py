from datetime import UTC, datetime

from app.Contexts.Shared.Domain.ValueObject.DateTimeValueObject import (
    DateTimeValueObject,
)


class Clock:
    def now(self) -> datetime:
        return datetime.now(UTC)

    def get_date_range(self, date_range: str) -> str:
        return DateTimeValueObject.now().to_date_string()
