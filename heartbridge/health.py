"""Module responsible for parsing input data from the iOS Shortcuts app,
and coordinating exports of that data.
"""

from .data import BaseHealthReading, GenericHealthReading
from .exceptions import ValidationError, LoadingError
from .export import export_filepath
from .constants import (
    EXPORT_CLS_MAP,
    READING_MAPPING,
    REQUIRED_FIELDS,
    LEGACY_RECORD_TYPE,
    DATE_PARSE_STRING,
)
from typing import List
from datetime import datetime
import warnings


class Health:
    """Coordinates parsing health data from Shortcuts, and stores a collection
    of parsed data to be exported.
    """

    def __init__(self, output_dir: str = None, output_format: str = None):
        self.output_dir = output_dir
        self.output_format = output_format
        self.readings = None
        self.reading_type_slug = None

    def load_from_shortcuts(self, data: dict) -> None:
        """Validates and loads data from the iOS Shortcuts app into a list of HealthReading
        instances.

        Args:
            data: The dictionary containing readings after data deserialization
        """

        # Infer reading type from input dictionary:
        reading_type = self._extract_record_type(data)

        # In cases where there's only one record, Shortcuts will send a string instead of a list.
        # We'll check if this happened and coerce everything into a list, before parsing.
        if reading_type == LEGACY_RECORD_TYPE:
            if (type(data["hrDates"]) == str) and (type(data["hrValues"]) == str):
                data["hrDates"] = [data["hrDates"]]
                data["hrValues"] = [data["hrValues"]]
        else:
            if (type(data["dates"]) == str) and (type(data["values"]) == str):
                data["dates"] = [data["dates"]]
                data["values"] = [data["values"]]

        if self._validate_input_fields(data, reading_type):
            self.reading_type_slug = reading_type
            self.readings = self._parse_shortcuts_data(data=data)
        else:
            raise ValidationError("Could not validate input data from Shortcuts")

    def export(self) -> str:
        """Depending on the `output_format`, calls the correct export functions
        and returns a path to the file created.
        """

        # Generate filename based on record type and date range:
        filename = "{}-{}".format(self.reading_type_slug, self._string_date_range())
        filepath = export_filepath(filename, self.output_dir, self.output_format)
        # Use the correct export class to export data, based on output format:
        exporter = EXPORT_CLS_MAP[self.output_format]
        # Return the full path of the file exported:
        export_filename = exporter().readings_to_file(self.readings, filepath)
        return export_filename

    def _parse_shortcuts_data(self, data: dict) -> List[BaseHealthReading]:
        """Parses input data from Shortcuts, and returns a list of health reading instances
        based on the type of input data. The list is ordered by timestamp (ascending).

        Args:
            data: Input data from shortcuts (as a dictionary)
        """

        reading_cls = READING_MAPPING.get(self.reading_type_slug, GenericHealthReading)

        date_key, value_key = ("dates", "values")
        if self.reading_type_slug == "heart-rate-legacy":
            date_key, value_key = ("hrDates", "hrValues")

        dates = (datetime.strptime(x, DATE_PARSE_STRING) for x in data[date_key])
        values = (float(x) for x in data[value_key])

        readings = []

        for date, value in zip(dates, values):
            readings.append(reading_cls(**{"timestamp": date, "value": value}))

        return readings

    def _check_legacy(self, data: dict) -> bool:
        """Checks whether the data is coming from the original version of Heartbridge
        (the shortcut for that version sends different keys in the heart rate data)
        """
        if ("hrDates" in data) and ("hrValues" in data):
            warnings.warn(
                "This version of the Heartbridge shortcut will be deprecated soon, please install the new one on GitHub: https://github.com/mm/heartbridge",
                FutureWarning,
            )
            return True
        return False

    def _extract_record_type(self, data: dict) -> str:
        """Extracts and reformats the record type of data from Shortcuts, by
        reading whatever's stored in `data[type].`

        Example:
            If the data from Shortcuts includes `type`: "Heart Rate", this function
            will return "heart-rate".
        """
        reading_type = data.get("type")
        if not reading_type:
            if self._check_legacy(data):
                return "heart-rate-legacy"
            else:
                raise LoadingError(
                    "Shortcuts input data must include a type key indicating the type of health record"
                )
        else:
            return reading_type.lower().replace(" ", "-")

    def _validate_input_fields(self, data: dict, reading_type: str) -> bool:
        """Validates that:
        * Input data contains the correct keys for the given reading type
        * Input data shape is correct
        """
        fields = REQUIRED_FIELDS
        if reading_type == LEGACY_RECORD_TYPE:
            fields = ["hrDates", "hrValues"]
        if not set(fields).issubset(data.keys()):
            raise ValidationError(
                f"Data does not have all the required fields for this record type: {fields}"
            )
        if not self._validate_input_field_length(data=data, reading_type=reading_type):
            raise ValidationError(
                f"The lengths of both fields in {fields} must be equal."
            )

        return True

    def _validate_input_field_length(self, data: dict, reading_type: str) -> bool:
        """All data fields returned from Shortcuts should have the same shape (i.e.
        number of heart rate readings should match the number of dates)
        """
        fields = REQUIRED_FIELDS
        if reading_type == LEGACY_RECORD_TYPE:
            fields = ["hrDates", "hrValues"]
        content_lengths = [len(data[field]) for field in fields]
        return all(x == content_lengths[0] for x in content_lengths)

    def _string_date_range(self) -> str:
        """
        Using the list of HealthReadings in `readings`, determines the date range of data
        present. Two outputs are possible:

        1) Data for only one day: Will return the one day in month-day-year format: i.e. Dec16-2019
        2) Data spanning multiple days: Will return the range in month-day-year-month-day-year format: i.e. Dec16-2019-Dec20-2019
        """

        if not self.readings:
            raise LoadingError(
                "Cannot determine the date range of an empty set of data"
            )

        try:
            begin_date = self.readings[
                0
            ].timestamp  # gets first element of the tuple (datetime) from first item in list
            end_date = self.readings[-1].timestamp
        except Exception as e:
            raise LoadingError(
                "Failed to determine the date range for the data passed in: {}".format(
                    e
                )
            )

        begin_string = begin_date.strftime("%b%d-%Y")
        end_string = end_date.strftime("%b%d-%Y")

        if begin_string == end_string:
            return begin_string
        else:
            return "{0}-{1}".format(begin_string, end_string)
