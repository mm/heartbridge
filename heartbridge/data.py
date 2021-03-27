"""Entity definitions (data classes) for Heartbridge. Each
class is a different record type from the Health app.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(order=True)
class BaseHealthReading:
    timestamp: datetime


@dataclass(order=True)
class HeartRateReading(BaseHealthReading):
    heart_rate: float

    def to_dict(self):
        return {
            'timestamp': datetime.strftime(self.timestamp, '%Y-%m-%d %H:%M:%S'),
            'heartRate': round(self.heart_rate, 1)
        }

@dataclass(order=True)
class StepsReading(BaseHealthReading):
    step_count: int

    def to_dict(self):
        return {
            'timestamp': datetime.strftime(self.timestamp, '%Y-%m-%d %H:%M:%S'),
            'steps': self.step_count
        }


@dataclass(order=True)
class FlightsClimbedReading(BaseHealthReading):
    climbed: int

    def to_dict(self):
        return {
            'timestamp': datetime.strftime(self.timestamp, '%Y-%m-%d %H:%M:%S'),
            'steps': self.climbed
        }