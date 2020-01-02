import argparse, socket
from flask import Flask, request, make_response
from heart import *

app = Flask(__name__)

# Add command-line arguments:
parser = argparse.ArgumentParser(description = "Opens a temporary REST endpoint to send heart rate data from Shortcuts to your computer.")
parser.add_argument("--directory", help = "Set the output directory for exported files. Defaults to current directory.")
parser.add_argument("--type", help = "Set the output file type. Can be csv or json. Defaults to csv.", default = "csv")

@app.route('/heartrate', methods = ['POST'])
def process_health_data():
    if(request.is_json and valid_heart_json(request.json)):
            parsed_data = parse_heart_json(request.json)
            print(f"Received heart rate data with {len(parsed_data)} samples.")
            export_filename = export_data(parsed_data, args.directory, args.type)
            print('\033[92m'+f"Successfully exported data to {export_filename}"+'\033[0m')
            return make_response(('Success', 200))
    else:
        return make_response(('Invalid data', 400))

if __name__ == '__main__':
    args = parser.parse_args()
    print('\033[94m'+f'Now accepting POST requests at http://{socket.gethostname()}:5000/heartrate'+'\033[0m')
    app.run(debug=False, host='0.0.0.0')