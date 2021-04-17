"""Constants used throughout Heartbridge (mainly for field mapping or validation)
"""

from .data import (
    CyclingDistanceReading,
    HeartRateReading,
    HeartRateVariabilityReading,
    RestingHeartRateReading,
    StepsReading,
    FlightsClimbedReading,
)
from .export import CSVExporter, JSONExporter


EXPORT_CLS_MAP = {"csv": CSVExporter, "json": JSONExporter}

READING_MAPPING = {
    "heart-rate": HeartRateReading,
    "heart-rate-legacy": HeartRateReading,
    "resting-heart-rate": RestingHeartRateReading,
    "heart-rate-variability": HeartRateVariabilityReading,
    "cycling-distance": CyclingDistanceReading,
    "steps": StepsReading,
    "flights-climbed": FlightsClimbedReading,
}

REQUIRED_FIELDS = ["dates", "values"]
LEGACY_RECORD_TYPE = "heart-rate-legacy"
DATE_PARSE_STRING = "%Y-%m-%d %H:%M:%S"
