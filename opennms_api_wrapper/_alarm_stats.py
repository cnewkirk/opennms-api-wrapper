"""Alarm Statistics REST API – /rest/stats/alarms."""


class AlarmStatsMixin:
    def get_alarm_stats(self, **filters):
        """Return alarm statistics.

        Args:
            **filters: Additional Hibernate query filters passed directly as query parameters (e.g. ``severity="MAJOR"``).
                Supports the same filter parameters as ``get_alarms()``.
        """
        return self._get("stats/alarms", params=filters)

    def get_alarm_stats_by_severity(self, severities: list = None):
        """Return alarm statistics grouped by severity.

        Args:
            severities: Optional list of severity strings to include,
                e.g. ``["MAJOR", "CRITICAL"]``.
        """
        params = {}
        if severities:
            params["severities"] = ",".join(severities)
        return self._get("stats/alarms/by-severity", params=params)
