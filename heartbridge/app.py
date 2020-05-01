import argparse, socket
from heartbridge import heart, server

# Add command-line arguments:
parser = argparse.ArgumentParser(description = "Opens a temporary REST endpoint to send heart rate data from Shortcuts to your computer.")
parser.add_argument("--directory", help = "Set the output directory for exported files. Defaults to current directory.")
parser.add_argument("--type", help = "Set the output file type. Can be csv or json. Defaults to csv.", default = "csv")
parser.add_argument("--port", help = "Set the port to listen for requests on. Defaults to 8888.", default = 8888)

def process_health_data(heartrate_dict, output_dir = None, output_format = None):
    """
    Processes heart rate data received over the HTTP endpoint, and coordinates exporting it to a CSV/JSON file.
    Will print informational messages about where the file was exported. Returns True in the case of a success, False otherwise.

    Arguments:
        * heartrate_dict: The deserialized JSON of heart rate dates / readings captured by the HTTP endpoint.
    """

    if heart.valid_heart_json(heartrate_dict):
        # If the passed in dictionary contains the appropriate keys and passes other checks, process it.
        parsed_data = heart.parse_heart_json(heartrate_dict)

        if parsed_data:
            # If there was data to parse, export it to a CSV or JSON file.
            print(f"Received heart rate data with {len(parsed_data)} samples.")
            export_filename = heart.export_data(parsed_data, output_dir, output_format)

            if export_filename:
                # Print the filename to console, in green and return True to indicate success
                print('\033[92m'+f"Successfully exported data to {export_filename}"+'\033[0m')
                return True
    
    return False

def check_args(args):
    """
    Validates command-line arguments passed in to the script.
    In particular, ensures the --type argument is one of csv or json.
    Returns True if checks pass, False otherwise.
    """
    
    if(args.type in ['csv', 'json']):
        return True
    else:
        print("Please specify your file type with --type as csv or json.")
        return False

def main():  
    # These will get set to the values passed in via the CLI if this script is run as the main module (i.e. not imported)
    output_dir = None
    output_format = None

    args = parser.parse_args()
    # If a user passes in CSV/JSON, correct it to csv/json
    args.type = args.type.lower()

    if check_args(args):
        # These are referenced in the process_health_data function:
        output_dir = args.directory
        output_format = args.type
        try:
            # This loop will create an HTTPServer instance to listen for incoming POST data from iOS Shortcuts.
            # Once data is received and deserialized, it is returned and the instance is deleted.
            # The instance is created again to listen for more data until the a keyboard interrupt is received.
            while True:
                # Listen on the port specified for a POST request containing the heart rate data payload
                output_data = server.run(port=int(args.port))
                # Process the data, exporting it to the directory/file type of choosing
                success = process_health_data(output_data, output_dir = output_dir, output_format = output_format)
                if not success:
                    print("Health data processing failed.")
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, stopping.")