"""
Main application logic. Parses command line arguments, starts
the HTTP server and processes JSON data from Shortcuts when
```cli()``` is run.
"""

import socket, logging, json
import uvicorn
import click
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from heartbridge.health import Health
from heartbridge.exception_handlers import EXCEPTION_HANDLER_MAPPING

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)


async def capture_health_data(request):
    try:
        health_data = await request.json()
    except json.decoder.JSONDecodeError:
        logging.error(
            "Error parsing JSON data; ensure valid JSON was sent to the endpoint"
        )
        return JSONResponse(
            {"message": "Could not read JSON data from Shortcuts"}, status_code=400
        )

    record_type = health_data.get("type", "health")
    health = Health(app.state.OUTPUT_DIRECTORY, app.state.OUTPUT_FORMAT)

    health.load_from_shortcuts(health_data)

    click.echo(
        "\u001b[33m\U0001F49B"
        + f" Detected {record_type} data with {len(health.readings)} samples."
        + "\033[0m"
    )
    if len(health.readings) > 0:
        export_filename = health.export()
        click.echo(
            "\033[92m\U00002705"
            + f" Successfully exported data to {export_filename}"
            + "\033[0m"
        )
        return JSONResponse({"message": "Data exported successfully"}, status_code=200)
    else:
        click.echo(
            "No data was found in body from Shortcuts. Export will not continue."
        )
        return JSONResponse(
            {
                "message": "No data was passed in the payload from Shortcuts; no data exported"
            },
            status_code=400,
        )


routes = [Route("/", endpoint=capture_health_data, methods=["POST"])]

app = Starlette(
    debug=False, routes=routes, exception_handlers=EXCEPTION_HANDLER_MAPPING
)


@click.command()
@click.option(
    "--directory",
    default=None,
    help="Set the output directory for exported files. Defaults to current directory. Will create directory if it does not already exist.",
    type=click.Path(exists=False, file_okay=False),
)
@click.option(
    "--type",
    default="csv",
    help="Set the output file type. Can be csv or json. Defaults to csv.",
    type=click.Choice(["csv", "json"]),
)
@click.option(
    "--port",
    default=8888,
    help="Set the port to listen for HTTP requests on. Defaults to 8888.",
    type=click.IntRange(1024, 65535),
)
def cli(directory: str, type: str, port: int):
    """Opens a temporary HTTP endpoint to send health data from Shortcuts to your computer."""
    hostname = socket.gethostname()
    # Set app state variables, which get used during export:
    app.state.OUTPUT_DIRECTORY = directory
    app.state.OUTPUT_FORMAT = type
    click.echo(
        "\U000026A1 Waiting to receive health data at http://{}:{}... (Press Ctrl+C to stop)".format(
            hostname, port
        )
    )
    uvicorn.run(app, host="0.0.0.0", log_level="error", access_log=False, port=port)
