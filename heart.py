import json, csv, os, pathlib
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

def string_date_range(hr_data):
    """
    Using the list of tuples from the `parse_heart_json` method, determines the date range
    of data present. Two outputs are possible:

    1) Data for only one day: Will return the one day in month-day-year format: i.e. dec16-2019
    2) Data spanning multiple days: Will return the range in month-day-year-month-day-year format: i.e. dec16-2019-dec20-2019
    """

    try:
        begin_date = hr_data[0][0] # gets first element of the tuple (datetime) from first item in list
        end_date = hr_data[-1][0] # gets first element of the tuple (datetime) from last item in list
    except IndexError:
        print("An empty list of tuples was passed -- check input data")
    
    begin_string = begin_date.strftime("%b%d-%Y")
    end_string = end_date.strftime("%b%d-%Y")

    if (begin_string == end_string):
        return(begin_string)
    else:
        return("{0}-{1}".format(begin_string, end_string))

def export_filepath(hr_data, output_dir, filetype):
    """
    Constructs the file path to be exported, based on user preferences.
    """

    # 1) Get the date range for this dataset
    filename = string_date_range(hr_data)

    # 2) Combine that with the directory path and file type passed in by the user
    if output_dir:
        fp = pathlib.Path(output_dir)
        if fp.is_dir():
            fp = fp / f'{filename}.{filetype}'
            print(fp)
        else:
            raise Exception("Path passed in to --directory does not exist!")
    else:
        fp = pathlib.Path.cwd() / f'{filename}.{filetype}'

    return(fp)

def export_data(hr_data, output_dir, filetype):
    """
    Exports the passed in list of tuples from `parse_heart_json` to either a JSON or CSV file.
    This function calls all other functions that:

    * Generate the file name based on the date range of the data passed in
    * Create a full file path to write to based on user input
    * Write the CSV/JSON file to the directory specified

    Returns the file path created if successful, None otherwise.
    """

    # Get the full file name to write to
    file_path = export_filepath(hr_data, output_dir, filetype)

    # Extract the extension from the filename
    extension = file_path.suffix

    if (extension == ".csv"):
        return(write_csv(hr_data, file_path))
    elif (extension == ".json"):
        return(write_json(hr_data, file_path))
    else:
        return None






