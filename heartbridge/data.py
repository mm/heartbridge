"""Entity definitions (data classes) for Heartbridge. Each
class is a different record type from the Health app.
"""

from dataclasses import dataclass, fields, InitVar
from datetime import datetime

@dataclass(order=True)
class BaseHealthReading:
    timestamp: datetime
    value: InitVar[str] = None

    @property
    def field_names(self):
        return [x.name for x in fields(self)]

    @property
    def timestamp_string(self) -> str:
        return datetime.strftime(self.timestamp, '%Y-%m-%d %H:%M:%S')

@dataclass(order=True)
class GenericHealthReading(BaseHealthReading):
    reading: str = None

    def to_dict(self):
        return {
            'timestamp': self.timestamp_string,
            'reading': self.reading
        }

    def __post_init__(self, value):
        self.reading = value

@dataclass(order=True)
class HeartRateReading(BaseHealthReading):
    heart_rate: float = None

    def to_dict(self):
        return {
            'timestamp': self.timestamp_string,
            'heart_rate': round(self.heart_rate, 1)
        }

    def __post_init__(self, value):
        self.heart_rate = int(value)

@dataclass(order=True)
class StepsReading(BaseHealthReading):
    step_count: int = None

    def to_dict(self):
        return {
            'timestamp': self.timestamp_string,
            'step_count': self.step_count
        }

    def __post_init__(self, value):
        self.step_count = int(value)


@dataclass(order=True)
class FlightsClimbedReading(BaseHealthReading):
    climbed: int = None

    def to_dict(self):
        return {
            'timestamp': self.timestamp_string,
            'climbed': self.climbed
        }

    def __post_init__(self, value):
        self.climbed = int(value)