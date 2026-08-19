"""Alarm Statistics REST API – /rest/stats/alarms."""
from ._base import _OpenNMSBase
from typing import Optional


class AlarmStatsMixin(_OpenNMSBase):
    def get_alarm_stats(self, **filters):
        """Return alarm statistics.

        Args:
            **filters: Additional Hibernate query filters passed directly as query parameters (e.g. ``severity="MAJOR"``).
                Supports the same filter parameters as ``get_alarms()``.
        """
        return self._get("stats/alarms", params=filters)

    def get_alarm_stats_by_severity(self, severities: Optional[list] = None):
        """Return alarm statistics grouped by severity.

        Args:
            severities: Optional list of severity strings to include,
                e.g. ``["MAJOR", "CRITICAL"]``.
        """
        params = {}
        if severities:
            params["severities"] = ",".join(severities)
        return self._get("stats/alarms/by-severity", params=params)
