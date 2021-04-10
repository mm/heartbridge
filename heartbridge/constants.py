"""Constants used throughout Heartbridge (mainly for field mapping or validation)
"""

from .data import HeartRateReading, StepsReading, FlightsClimbedReading
from .export import CSVExporter, JSONExporter


EXPORT_CLS_MAP = {
    'csv': CSVExporter,
    'json': JSONExporter
}

READING_MAPPING = {
    'heart-rate': HeartRateReading,
    'heart-rate-legacy': HeartRateReading,
    'steps': StepsReading,
    'flights-climbed': FlightsClimbedReading
}

REQUIRED_FIELDS = ['dates', 'values']
LEGACY_RECORD_TYPE = 'heart-rate-legacy'
DATE_PARSE_STRING = '%Y-%m-%d %H:%M:%S'