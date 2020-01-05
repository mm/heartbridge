import argparse, socket
from flask import Flask, request, make_response, jsonify
from heart import *

app = Flask(__name__)

# Add command-line arguments:
parser = argparse.ArgumentParser(description = "Opens a temporary REST endpoint to send heart rate data from Shortcuts to your computer.")
parser.add_argument("--directory", help = "Set the output directory for exported files. Defaults to current directory.")
parser.add_argument("--type", help = "Set the output file type. Can be csv or json. Defaults to csv.", default = "csv")

# These will get set to the values passed in via the CLI if this script is run as the main module (i.e. not imported)
output_dir = None
output_format = None

@app.route('/heartrate', methods = ['POST'])
def process_health_data():
    if(request.is_json and valid_heart_json(request.json)):
            parsed_data = parse_heart_json(request.json)

            if parsed_data:
                print(f"Received heart rate data with {len(parsed_data)} samples.")
                export_filename = export_data(parsed_data, output_dir, output_format)

                if export_filename:
                    print('\033[92m'+f"Successfully exported data to {export_filename}"+'\033[0m')
                    return make_response((jsonify({'status': 'Successful', 'fileName': export_filename, 'numberOfSamples': len(parsed_data)}), 200))
    
    return make_response(('Invalid data', 400))

def check_args(args):
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
        print('\033[94m'+f'Now accepting POST requests at http://{socket.gethostname()}:5000/heartrate'+'\033[0m')
        app.run(debug=False, host='0.0.0.0', port=5000)