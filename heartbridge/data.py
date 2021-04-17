"""Entity definitions (data classes) for Heartbridge. Each
class is a different record type from the Health app.
"""

from dataclasses import dataclass, fields, InitVar
from typing import ClassVar
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
        return datetime.strftime(self.timestamp, "%Y-%m-%d %H:%M:%S")

    def get_value(self):
        """Gets the value of a health reading, determined by the `value_attribute`
        class variable.
        """
        if self.__annotations__.get("value_attribute"):
            value_key = getattr(self, "value_attribute")
            return self.__getattribute__(value_key)
        return None

    def to_dict(self):
        """Converts the data object to a dictionary. Call only
        on a subclass of BaseHealthReading.
        """
        if self.__annotations__.get("value_attribute"):
            value_key = getattr(self, "value_attribute")
            return {
                "timestamp": self.timestamp_string,
                value_key: self.__getattribute__(value_key),
            }


@dataclass(order=True)
class GenericHealthReading(BaseHealthReading):
    reading: str = None
    value_attribute: ClassVar[str] = "reading"

    def __post_init__(self, value):
        self.reading = value


@dataclass(order=True)
class HeartRateReading(BaseHealthReading):
    heart_rate: float = None
    value_attribute: ClassVar[str] = "heart_rate"

    def __post_init__(self, value):
        self.heart_rate = int(value)


@dataclass(order=True)
class RestingHeartRateReading(BaseHealthReading):
    resting_heart_rate: int = None
    value_attribute: ClassVar[str] = "resting_heart_rate"

    def __post_init__(self, value):
        self.resting_heart_rate = int(value)


@dataclass(order=True)
class HeartRateVariabilityReading(BaseHealthReading):
    heart_rate_variability: float = None
    value_attribute: ClassVar[str] = "heart_rate_variability"

    def __post_init__(self, value):
        self.heart_rate_variability = round(float(value), 2)


@dataclass(order=True)
class StepsReading(BaseHealthReading):
    step_count: int = None
    value_attribute: ClassVar[str] = "step_count"

    def __post_init__(self, value):
        self.step_count = int(value)


@dataclass(order=True)
class FlightsClimbedReading(BaseHealthReading):
    climbed: int = None
    value_attribute: ClassVar[str] = "climbed"

    def __post_init__(self, value):
        self.climbed = int(value)


@dataclass(order=True)
class CyclingDistanceReading(BaseHealthReading):
    distance_cycled: float = None
    value_attribute: ClassVar[str] = "distance_cycled"

    def __post_init__(self, value):
        self.distance_cycled = float(value)
