"""Custom exceptions for Heartbridge.
"""


class ValidationError(Exception):
    """Raised during Shortcuts data validation."""

    pass


class ExportError(Exception):
    """Raised while exporting data to another format"""

    pass


class LoadingError(Exception):
    """Raised during data loading, but not related to validation."""

    pass
