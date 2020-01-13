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
    
    print("The JSON file passed in is missing data -- please check the output from Shortcuts.")
    return False

def parse_heart_json(input_json):
    """
    Input JSON from Shortcuts currently contains two keys:
    - hrDates: Contains an array of all timestamps (ascending order)
    - hrValues: Contains an array of all heart rates (sorted by timestamp, ascending)

    This converts the dictionary into a list of tuples: each containing a timestamp
    and the corresponding HR reading. If parsing fails, None is returned.
    """

    try:
        hr_dates = [datetime.strptime(x, '%d-%m-%Y %H:%M:%S') for x in input_json['hrDates']]
        hr_values = [float(x) for x in input_json['hrValues']]
        all_data = list(zip(hr_dates, hr_values)) 

        if(len(all_data) == 0):
            print("No health samples found in data. Nothing will be exported.")

        return(all_data)
    except ValueError as ve:
        print("Error parsing the dates or values returned from the Shortcuts app: {}".format(ve))
        return(None)

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
        print("An error occured while writing the CSV file: {}".format(e))
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
        print("An error occured while writing the JSON file: {}".format(e))
        return(None)

def string_date_range(hr_data):
    """
    Using the list of tuples from the `parse_heart_json` method, determines the date range
    of data present. Two outputs are possible:

    1) Data for only one day: Will return the one day in month-day-year format: i.e. Dec16-2019
    2) Data spanning multiple days: Will return the range in month-day-year-month-day-year format: i.e. Dec16-2019-Dec20-2019
    """

    try:
        begin_date = hr_data[0][0] # gets first element of the tuple (datetime) from first item in list
        end_date = hr_data[-1][0] # gets first element of the tuple (datetime) from last item in list
    except IndexError:
        print("An empty list of tuples was passed -- please check input data")
        return(None)
    except Exception as e:
        print("Failed to determine the date range for the data passed in: {}".format(e))
        return(None)
    
    begin_string = begin_date.strftime("%b%d-%Y")
    end_string = end_date.strftime("%b%d-%Y")

    if (begin_string == end_string):
        return(begin_string)
    else:
        return("{0}-{1}".format(begin_string, end_string))

def export_filepath(hr_data, output_dir, filetype):
    """
    Constructs the file path to be exported, based on user preferences.
    Will return None if the file path could not be constructed.
    """

    # 1) Get the date range for this dataset
    filename = string_date_range(hr_data)

    # 2) Combine that with the directory path and file type passed in by the user
    if filename:
        if output_dir:
            # File will reside in the directory passed in by the user
            fp = pathlib.Path(output_dir)
            if fp.is_dir():
                fp = fp / f'{filename}.{filetype}'
            else:
                print("Path passed in to --directory does not exist!")
        else:
            # File will reside in the current working directory of the script
            fp = pathlib.Path.cwd() / f'{filename}.{filetype}'
        return(fp)
    return(None)

def export_data(hr_data, output_dir, filetype):
    """
    Exports the passed in list of tuples from `parse_heart_json` to either a JSON or CSV file.
    This function calls all other functions that:

    * Generate the file name based on the date range of the data passed in
    * Create a full file path to write to based on user input
    * Write the CSV/JSON file to the directory specified

    Returns the file path created if successful, None otherwise.
    """

    # Check if the output directory and file type haven't been specified.
    # If this is the case, the application is just being imported (likely for testing),
    # so the behaviour is to not write anything to disk (a dry run)

    if (output_dir is None and filetype is None):
        # Get the file name without an extension, and return that instead
        fn = string_date_range(hr_data)
        return(fn)
    else:
        # Get the full file name to write to
        file_path = export_filepath(hr_data, output_dir, filetype)

        if file_path:
            if (filetype == "csv"):
                return(write_csv(hr_data, file_path))
            elif (filetype == "json"):
                return(write_json(hr_data, file_path))
        
        print("No data was written to disk due to an error -- please check the output above.")
        return None






