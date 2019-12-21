import json, csv, os
import pandas as pd
from datetime import datetime

def valid_heart_json(input_json):
    """
    Checks to make sure input JSON is valid and contains the appropriate keys.
    Will also check to make sure the number of dates passed in matches the number
    of readings.

    Returns True if all checks passed, False otherwise.
    """

    if(type(input_json) is dict):
        if('hrDates' in input_json and 'hrValues' in input_json):
            if(len(input_json['hrDates']) == len(input_json['hrValues'])):
                return True

    return False

def parse_heart_json(input_json):
    """
    Input JSON from Shortcuts currently contains two keys:
    - hrDates: Contains an array of all timestamps (ascending order)
    - hrValues: Contains an array of all heart rates (sorted by timestamp, ascending)

    This converts the dictionary into a list of tuples: each containing a timestamp
    and the corresponding HR reading.
    """

    hr_dates = [datetime.strptime(x, '%d-%m-%Y %H:%M:%S') for x in input_json['hrDates']]
    hr_values = [float(x) for x in input_json['hrValues']]

    return(list(zip(hr_dates, hr_values)))

def write_csv(hr_data, filename):
    """
    Using the list of tuples created from `parse_heart_json`, generates a CSV file and saves it
    to the directory of choice.

    Returns the file path if successful, None otherwise.
    """
    
    try:
        with open(filename, 'w', newline = '') as hr_export:
            writer = csv.writer(hr_export)
            writer.writerow(["Timestamp", "HeartRate"])
            writer.writerows(hr_data)
            return(os.path.realpath(hr_export.name))
    except Exception as e:
        return(None)

def write_json(hr_data, filename):
    """
    Using the list of tuples created from `parse_heart_json`, generates a CSV file and saves it
    to the directory of choice.

    Returns the file path if successful, None otherwise.
    """

    # Convert our list of tuples to a list of dicts
    hr_dicts = [{'timestamp': datetime.strftime(x[0], '%d-%m-%Y %H:%M:%S'), 'heartRate': x[1]} for x in hr_data]
    
    # Serialize this to a JSON formatted stream and write it to a file
    try:
        with open(filename, 'w') as hr_export:
            json.dump(hr_dicts, hr_export)
            return(os.path.realpath(hr_export.name))
    except Exception as e:
        return None

def to_dataframe(hr_data):
    """
    Using the list of tuples created from `parse_heart_json`, constructs a Pandas dataframe
    and returns it.
    """

    return pd.DataFrame(data = hr_data, columns = ["Timestamp", "HeartRate"])






