"""opennms_api_wrapper – a thin Python wrapper for the OpenNMS REST API."""
from .client import OpenNMS
from ._exceptions import (
    OpenNMSError,
    OpenNMSHTTPError,
    BadRequestError,
    AuthenticationError,
    ForbiddenError,
    NotFoundError,
    ConflictError,
    ServerError,
)
from importlib.metadata import version, PackageNotFoundError

__all__ = [
    "OpenNMS",
    "OpenNMSError",
    "OpenNMSHTTPError",
    "BadRequestError",
    "AuthenticationError",
    "ForbiddenError",
    "NotFoundError",
    "ConflictError",
    "ServerError",
]

try:
    __version__ = version("opennms-api-wrapper")
except PackageNotFoundError:
    __version__ = "unknown"
