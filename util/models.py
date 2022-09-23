from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class TargetDatetime:
    target: datetime

    @property
    def remaining(self) -> timedelta:
        now = datetime.now()
        remaining = self.target - now
        return remaining

    @property
    def remaining_days(self) -> float:
        return self.remaining.total_seconds() / 86400

    @property
    def remaining_hours(self) -> float:
        return self.remaining.total_seconds() / 3600

    @property
    def remaining_minutes(self) -> float:
        return self.remaining.total_seconds() / 60

    @property
    def remaining_seconds(self) -> float:
        return self.remaining.total_seconds()

    @property
    def remaining_short_humanized(self) -> str:
        def format(value: float, suffix: str = "") -> str:
            return f"{value:.2f}{suffix}" if value == 1 else f"{value:.2f} {suffix}s"

        if self.remaining_days >= 1:
            return format(self.remaining_days, "day")
        if self.remaining_hours >= 1:
            return format(self.remaining_hours, "hr")
        if self.remaining_minutes >= 1:
            return format(self.remaining_minutes, "min")
        return format(self.remaining_seconds, "sec")
