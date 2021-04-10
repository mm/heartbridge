"""Module responsible for exporting health readings to another file type
(e.g JSON or CSV)
"""

import json, csv, os, pathlib
from abc import ABC, abstractmethod
from typing import List
from .data import BaseHealthReading

class ExporterBase(ABC):
    """Abstract base class for all health reading exporters.
    """

    @abstractmethod
    def readings_to_file(self, data: List[BaseHealthReading], filename: str) -> str:
        """Exports a collection of health readings to a file. All classes implementing
        this method should return the file path.
        """
        pass


class CSVExporter(ExporterBase):

    def readings_to_file(self, data: List[BaseHealthReading], filename: str) -> str:
        """Exports a collection of readings to a CSV file, and returns the file path.
        """
        try:
            all_readings = [reading.to_dict() for reading in data]
            with open(filename, 'w', newline = '') as export_file:
                writer = csv.DictWriter(export_file, fieldnames=data[0].field_names)
                writer.writeheader()
                writer.writerows(all_readings)
                return(os.path.realpath(export_file.name))
        except Exception as e:
            print("An error occured while writing the CSV file: {}".format(e))
            return(None)
            


class JSONExporter(ExporterBase):

    def readings_to_file(self, data: List[BaseHealthReading], filename: str) -> str:
        """Exports a collection of readings to a JSON file, and returns the file path.
        """
        try:
            all_readings = [reading.to_dict() for reading in data]
            with open(filename, 'w') as export_file:
                json.dump(all_readings, export_file)
                return(os.path.realpath(export_file.name))
        except Exception as e:
            print("An error occured while writing the JSON file: {}".format(e))
            return(None)
        

def export_filepath(filename, output_dir, filetype):
    """
    Constructs the file path to be exported, based on user preferences.
    Will return None if the file path could not be constructed. Will check if
    the target directory exists beforehand and create if necessary.

    Arguments:
        * filename (str): The name of the file to be exported (no extension)
        * output_dir (str): The directory to export the file to
        * filetype (str): Either csv or json
    """

    if filename and filetype:
        if output_dir:
            # File will reside in the directory passed in by the user
            fp = pathlib.Path(output_dir)
            if fp.is_dir():
                # If the user passed in a directory that already exists, great! Construct a full path based on it.
                fp = fp / f'{filename}.{filetype}'
            elif fp.is_file():
                # If the user passed a file by accident, reject it.
                print("Directory passed into --directory is a file! Please specify a directory.")
                return None
            else:
                # The directory must not exist yet -- create it and then construct the path.
                try:
                    os.mkdir(fp)
                    fp = fp / f'{filename}.{filetype}'
                except Exception as e:
                    print("Exception occured while creating directory: {}".format(e))
                    return None                
        else:
            # File will reside in the current working directory and will return filename.filetype
            fp = str(filename)+'.'+str(filetype)
        return fp
    return None