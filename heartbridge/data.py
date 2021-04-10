"""Entity definitions (data classes) for Heartbridge. Each
class is a different record type from the Health app.
"""

from dataclasses import dataclass, fields
from datetime import datetime


@dataclass(order=True)
class BaseHealthReading:
    timestamp: datetime
    value: str

    @property
    def field_names(self):
        return [x.name for x in fields(self)]

    def to_dict(self):
        return {
            'timestamp': datetime.strftime(self.timestamp, '%Y-%m-%d %H:%M:%S'),
            'value': self.value
        }


@dataclass(order=True)
class HeartRateReading(BaseHealthReading):
    heart_rate: float = None

    def to_dict(self):
        return {
            'timestamp': datetime.strftime(self.timestamp, '%Y-%m-%d %H:%M:%S'),
            'heart_rate': round(self.heart_rate, 1)
        }

    def __post_init__(self):
        self.heart_rate = float(self.value)

@dataclass(order=True)
class StepsReading(BaseHealthReading):
    step_count: int = None

    def to_dict(self):
        return {
            'timestamp': datetime.strftime(self.timestamp, '%Y-%m-%d %H:%M:%S'),
            'step_count': self.step_count
        }

    def __post_init__(self):
        self.step_count = int(self.value)


@dataclass(order=True)
class FlightsClimbedReading(BaseHealthReading):
    climbed: int = None

    def to_dict(self):
        return {
            'timestamp': datetime.strftime(self.timestamp, '%Y-%m-%d %H:%M:%S'),
            'climbed': self.climbed
        }

    def __post_init__(self):
        self.climbed = int(self.value)