"""Module responsible for parsing input data from the iOS Shortcuts app,
and coordinating exports of that data.
"""

from .data import BaseHealthReading, HeartRateReading, StepsReading, FlightsClimbedReading
from typing import Generator
from datetime import datetime


READING_MAPPING = {
    'heartrate': HeartRateReading,
    'steps': StepsReading,
    'flights': FlightsClimbedReading
}

SHORTCUTS_INPUT_FIELDS = {
    'heartrate': ('hrDates', 'hrValues')
}

DATE_PARSE_STRING = '%Y-%m-%d %H:%M:%S'


class Health:

    def __init__(self, output_dir: str = None, output_format: str = None):
        self.output_dir = output_dir
        self.output_format = output_format

    
    def validate_input_fields(self, data: dict, reading_type: str) -> bool:
        """Validates that:
            * Input data contains the correct keys for the given reading type
            * Input data shape is correct
        """

        fields = SHORTCUTS_INPUT_FIELDS.get(reading_type)
        if not fields:
            # TODO: We'll probably raise a custom error here
            raise NotImplementedError
        if not set(fields).issubset(data.keys):
            raise ValueError
        if not self._validate_input_field_length(data=data, reading_type=reading_type):
            raise ValueError

        return True


    def parse_shortcuts_data(self, data:dict, reading_type: str) -> Generator[HeartRateReading]:
        reading_cls = READING_MAPPING.get(reading_type)
        if not reading_cls:
            raise NotImplementedError
        
        dates = [datetime.strptime(x, DATE_PARSE_STRING) for x in data['hrDates']]
        values = [float(x) for x in data['hrValues']]

        for date, value in zip(dates, values):
            yield HeartRateReading(timestamp=date, heart_rate=value)
        

    def _validate_input_field_length(self, data:dict, reading_type: str) -> bool:
        """All data fields returned from Shortcuts should have the same shape (i.e.
        number of heart rate readings should match the number of dates)
        """
        fields = SHORTCUTS_INPUT_FIELDS.get(reading_type)
        content_lengths = [len(data[field]) for field in fields]
        return all(x == content_lengths[0] for x in content_lengths)