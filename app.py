import argparse, socket
from heart import *
import server

# Add command-line arguments:
parser = argparse.ArgumentParser(description = "Opens a temporary REST endpoint to send heart rate data from Shortcuts to your computer.")
parser.add_argument("--directory", help = "Set the output directory for exported files. Defaults to current directory.")
parser.add_argument("--type", help = "Set the output file type. Can be csv or json. Defaults to csv.", default = "csv")
parser.add_argument("--port", help = "Set the port to listen for requests on. Defaults to 8888.", default = 8888)

# These will get set to the values passed in via the CLI if this script is run as the main module (i.e. not imported)
output_dir = None
output_format = None

def process_health_data(heartrate_dict):
    """
    Processes heart rate data received over the HTTP endpoint, and coordinates exporting it to a CSV/JSON file.
    Does not return anything, but will print informational messages about where the file was exported.
    """

    if(valid_heart_json(heartrate_dict)):
        parsed_data = parse_heart_json(heartrate_dict)

        if parsed_data:
            print(f"Received heart rate data with {len(parsed_data)} samples.")
            export_filename = export_data(parsed_data, output_dir, output_format)

            if export_filename:
                print('\033[92m'+f"Successfully exported data to {export_filename}"+'\033[0m')

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

if __name__ == '__main__':
    args = parser.parse_args()
    # If a user passes in CSV/JSON, correct it to csv/json
    args.type = args.type.lower()

    if check_args(args):
        output_dir = args.directory
        output_format = args.type
        try:
            while True:
                output_data = server.run(port=int(args.port))
                process_health_data(output_data)
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received. Stopping...")