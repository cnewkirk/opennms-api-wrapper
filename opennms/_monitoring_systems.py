"""Monitoring Systems REST API – /rest/monitoringSystems."""


class MonitoringSystemsMixin:
    def get_monitoring_system(self):
        """Get the main monitoring system information."""
        return self._get("monitoringSystems/main")
