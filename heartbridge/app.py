"""
Main application logic. Parses command line arguments, starts
the HTTP server and processes JSON data from Shortcuts when
```main()``` is run.
"""

import argparse
import socket
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from heartbridge.health import Health


# Add command-line arguments:
parser = argparse.ArgumentParser(description = "Opens a temporary HTTP endpoint to send heart rate data from Shortcuts to your computer.")
parser.add_argument("--directory", help = "Set the output directory for exported files. Defaults to current directory. Will create directory if it doesn't already exist.")
parser.add_argument("--type", help = "Set the output file type. Can be csv or json. Defaults to csv.", default = "csv")
parser.add_argument("--port", help = "Set the port to listen for HTTP requests on. Defaults to 8888.", default = 8888)

async def capture_health_data(request):
    health_data = await request.json()
    process_health_data(health_data, app.state.OUTPUT_DIRECTORY, app.state.OUTPUT_FORMAT)
    return JSONResponse({'message': 'Data processed'})

routes = [
    Route("/", endpoint=capture_health_data, methods=['POST'])
]

app = Starlette(debug=False, routes=routes)

def process_health_data(heartrate_dict, output_dir = None, output_format = None):
    """
    Processes heart rate data received over the HTTP endpoint, and coordinates exporting it to a CSV/JSON file.
    Will print informational messages about where the file was exported. Returns True in the case of a success, False otherwise.

    Arguments:
        * heartrate_dict (dict): The deserialized JSON of heart rate dates / readings captured by the HTTP endpoint.
        * output_dir (str): The path of the directory to output files to
        * output_format (str): Either csv or json -- the file format the export will be in
    """

    health = Health(output_dir, output_format)

    # 1) Validate and parse data from Shortcuts:
    health.load_from_shortcuts(heartrate_dict)
    print(f"Loaded health data with {len(health.readings)} samples.")
    # 2) If there was data loaded in, create an export and print statistics:
    export_filename = health.export_to_file()

    if export_filename:
        # Print the filename to console, in green and return True to indicate success
        print('\033[92m'+f"Successfully exported data to {export_filename}"+'\033[0m')
        return True
    
    return False

def check_args(args):
    """
    Validates command-line arguments passed in to the script:
    * Ensures the --type argument is one of csv or json.
    * Ensures the port to listen on is between 1024 and 65535.

    Arguments:
        * args: The args namespace produced by ```parse_args```

    Returns True if checks pass, False otherwise.
    """
    errors = 0

    if(args.type not in ['csv', 'json']):
        errors += 1
        print("Please specify your file type with --type as csv or json.")
    
    if(int(args.port) <= 1023 or int(args.port) > 65535):
        errors += 1
        print("Please specify an integer port between 1024 and 65535.")

    if errors == 0:
        return True
    return False

def main():  
    # Parse arguments received from the command line:
    args = parser.parse_args()
    # If a user passes in CSV/JSON, correct it to csv/json
    args.type = args.type.lower()
    hostname = socket.gethostname()

    if check_args(args):
        app.state.OUTPUT_DIRECTORY = args.directory
        app.state.OUTPUT_FORMAT = args.type
        print("\U000026A1 Waiting to receive health data at http://{}:{}...".format(hostname, args.port))
        print("Press Ctrl+C to stop listening for new data.")
        uvicorn.run(app, host='0.0.0.0', log_level='error', access_log=False, port=int(args.port))