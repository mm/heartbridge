import json
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





