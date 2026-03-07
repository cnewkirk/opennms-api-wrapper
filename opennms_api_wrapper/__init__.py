"""opennms_api_wrapper – a thin Python wrapper for the OpenNMS REST API."""
from .client import OpenNMS
from importlib.metadata import version, PackageNotFoundError

__all__ = ["OpenNMS"]

try:
    __version__ = version("opennms-api-wrapper")
except PackageNotFoundError:
    __version__ = "unknown"
