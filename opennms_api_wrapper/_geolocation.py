"""Geolocation REST API v2 – /api/v2/geolocation."""
from __future__ import annotations
from ._base import _OpenNMSBase
from typing import Any, Optional


class GeolocationMixin(_OpenNMSBase):
    def get_geolocation_config(self):
        """Get the map/tile-server configuration.

        Returns:
            Dict with ``tileServerName``, ``tileServerUrl``, and
            ``options`` keys.
        """
        return self._get("geolocation/config", v2=True)

    def query_geolocations(self, strategy: str = "Alarms",
                           severity_filter: Optional[str] = None,
                           include_acknowledged_alarms:
                           Optional[bool] = None):
        """Query nodes with geographic locations and their status.

        Args:
            strategy: Status computation strategy — ``"Alarms"`` or
                ``"Outages"``.
            severity_filter: Only return nodes at or above this
                severity, e.g. ``"Major"``.
            include_acknowledged_alarms: Whether acknowledged alarms
                count toward node status.

        Returns:
            List of geolocation info dicts, or ``None`` for an empty
            result set (204 No Content).
        """
        body: dict[str, Any] = {"strategy": strategy}
        if severity_filter is not None:
            body["severityFilter"] = severity_filter
        if include_acknowledged_alarms is not None:
            body["includeAcknowledgedAlarms"] = (
                include_acknowledged_alarms)
        return self._post("geolocation", json_data=body, v2=True)
