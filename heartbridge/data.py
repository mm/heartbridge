"""Entity definitions (data classes) for Heartbridge. Each
class is a different record type from the Health app.
"""

from dataclasses import dataclass, fields
from datetime import datetime


@dataclass(order=True)
class BaseHealthReading:
    timestamp: datetime

    @property
    def field_names(self):
        return [x.name for x in fields(self)]


@dataclass(order=True)
class HeartRateReading(BaseHealthReading):
    heart_rate: float

    def to_dict(self):
        return {
            'timestamp': datetime.strftime(self.timestamp, '%Y-%m-%d %H:%M:%S'),
            'heart_rate': round(self.heart_rate, 1)
        }

@dataclass(order=True)
class StepsReading(BaseHealthReading):
    step_count: int

    def to_dict(self):
        return {
            'timestamp': datetime.strftime(self.timestamp, '%Y-%m-%d %H:%M:%S'),
            'step_count': self.step_count
        }


@dataclass(order=True)
class FlightsClimbedReading(BaseHealthReading):
    climbed: int

    def to_dict(self):
        return {
            'timestamp': datetime.strftime(self.timestamp, '%Y-%m-%d %H:%M:%S'),
            'climbed': self.climbed
        }