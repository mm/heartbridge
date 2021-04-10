"""
Main application logic. Parses command line arguments, starts
the HTTP server and processes JSON data from Shortcuts when
```cli()``` is run.
"""

import socket
import uvicorn
import click
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from heartbridge.health import Health

async def capture_health_data(request):
    health_data = await request.json()
    record_type = health_data.get('type')
    if record_type:
        print(f'Detected {record_type} data.')
    health = Health(app.state.OUTPUT_DIRECTORY, app.state.OUTPUT_FORMAT)
    health.load_from_shortcuts(health_data)
    print('\u001b[33m'+f'Loaded health data with {len(health.readings)} samples.'+'\033[0m')
    export_filename = health.export()
    if export_filename:
        # Print the filename to console, in green and return True to indicate success
        print('\033[92m'+f"Successfully exported data to {export_filename}"+'\033[0m')
    return JSONResponse({'message': 'Data processed'})

routes = [
    Route("/", endpoint=capture_health_data, methods=['POST'])
]

app = Starlette(debug=False, routes=routes)

@click.command()
@click.option('--directory', default=None, help="Set the output directory for exported files. Defaults to current directory. Will create directory if it doesn't already exist.")
@click.option('--type', default='csv', help='Set the output file type. Can be csv or json. Defaults to csv.', type=click.Choice(['csv', 'json']))
@click.option('--port', default=8888, help='Set the port to listen for HTTP requests on. Defaults to 8888.', type=click.IntRange(1024, 65535))
def cli(directory: str, type:str, port:int):
    """Opens a temporary HTTP endpoint to send health data from Shortcuts to your computer.
    """
    hostname = socket.gethostname()
    # Set app state variables, which get used during export:
    app.state.OUTPUT_DIRECTORY = directory
    app.state.OUTPUT_FORMAT = type
    print("\U000026A1 Waiting to receive health data at http://{}:{}...".format(hostname, port))
    print("Press Ctrl+C to stop listening for new data.")
    uvicorn.run(app, host='0.0.0.0', log_level='info', access_log=False, port=port)