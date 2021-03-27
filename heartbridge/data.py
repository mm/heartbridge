"""Entity definitions (data classes) for Heartbridge. Each
class is a different record type from the Health app.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class HeartRateReading:
    timestamp: datetime
    heart_rate: float

    def to_dict(self):
        return {
            'timestamp': datetime.strftime(self.timestamp, '%Y-%m-%d %H:%M:%S'),
            'heartRate': round(self.heart_rate, 1)
        }


@dataclass
class StepsReading:
    timestamp: datetime
    step_count: int

    def to_dict(self):
        return {
            'timestamp': datetime.strftime(self.timestamp, '%Y-%m-%d %H:%M:%S'),
            'steps': self.step_count
        }


@dataclass
class FlightsClimbedReading:
    timestamp: datetime
    climbed: int

    def to_dict(self):
        return {
            'timestamp': datetime.strftime(self.timestamp, '%Y-%m-%d %H:%M:%S'),
            'steps': self.climbed
        }