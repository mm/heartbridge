"""Module responsible for exporting health readings to another file type
(e.g JSON or CSV)
"""

import json, csv, os
from abc import ABC, abstractmethod
from typing import List
from .data import BaseHealthReading

class ExporterBase(ABC):
    """Abstract base class for all health reading exporters.
    """

    @abstractmethod
    def readings_to_file(self, data: List[BaseHealthReading], filename: str) -> str:
        """Exports a collection of health readings to a file.
        """
        pass


class CSVExporter(ExporterBase):

    def readings_to_file(self, data: List[BaseHealthReading], filename: str) -> str:
        """Exports a collection of readings to a CSV file.
        """
        try:
            all_readings = [reading.to_dict() for reading in data]
            with open(filename, 'w', newline = '') as export_file:
                writer = csv.DictWriter(export_file, fieldnames=data[0].field_names)
                writer.writerows(all_readings)
                return(os.path.realpath(export_file.name))
        except Exception as e:
            print("An error occured while writing the CSV file: {}".format(e))
            return(None)
            


class JSONExporter(ExporterBase):

    def readings_to_file(self, data: List[BaseHealthReading], filename: str) -> str:
        """Exports a collection of readings to a JSON file.
        """
        pass