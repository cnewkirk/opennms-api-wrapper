"""Monitoring Locations REST API – /rest/monitoringLocations."""
from ._base import _OpenNMSBase
from .types import MonitoringLocation


class MonitoringLocationsMixin(_OpenNMSBase):
    def get_monitoring_locations(self, limit: int = 10, offset: int = 0):
        """List all monitoring locations.

        Args:
            limit: Maximum number of results. Use ``0`` for all.
            offset: Number of results to skip (for pagination).
        """
        params = {"limit": limit, "offset": offset}
        return self._get("monitoringLocations", params=params)

    def get_monitoring_location(self, name: str):
        """Get a specific monitoring location by *name*."""
        return self._get(f"monitoringLocations/{name}")

    def get_default_monitoring_location(self):
        """Get the default monitoring location."""
        return self._get("monitoringLocations/default")

    def get_monitoring_location_count(self):
        """Return the number of monitoring locations."""
        return self._get("monitoringLocations/count")

    def create_monitoring_location(self, location: MonitoringLocation):
        """Create a new monitoring location.

        Args:
            location: Monitoring location definition.  See
                :class:`~opennms_api_wrapper.types.MonitoringLocation`
                for all available fields.
        """
        return self._post("monitoringLocations", json_data=location)

    def update_monitoring_location(self, name: str, data: dict):
        """Update a monitoring location.

        Args:
            name: Name of the monitoring location to update.
            data: Form-encoded key/value pairs to update.
        """
        return self._put(f"monitoringLocations/{name}", form_data=data)

    def delete_monitoring_location(self, name: str):
        """Delete a monitoring location."""
        return self._delete(f"monitoringLocations/{name}")
