"""Exception handlers for the Heartbridge Starlette application.
"""

import logging
from starlette.responses import JSONResponse
from heartbridge.exceptions import ValidationError, LoadingError, ExportError


async def loading_error(request, exc):
    logging.error(f"An issue occured while loading data: {exc}")
    return JSONResponse(
        {"message": "Issues occured while processing data"}, status_code=400
    )


async def validation_error(request, exc):
    logging.error(f"Validation error occured while loading data: {exc}")
    return JSONResponse({"message": "Invalid data passed"}, status_code=422)


async def export_error(request, exc):
    logging.error(f"Error exporting data to file: {exc}")
    return JSONResponse(
        {"message": "An issue occured during data export"}, status_code=500
    )


EXCEPTION_HANDLER_MAPPING = {
    ValidationError: validation_error,
    LoadingError: loading_error,
    ExportError: export_error,
}
