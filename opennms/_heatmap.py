"""Heatmap REST API – /rest/heatmap (read-only)."""
from ._base import _OpenNMSBase


class HeatmapMixin(_OpenNMSBase):
    # ==================================================================
    # Outage-based heatmap
    # ==================================================================

    def get_heatmap_outages_categories(self):
        """Return outage heatmap data grouped by category."""
        return self._get("heatmap/outages/categories")

    def get_heatmap_outages_foreign_sources(self):
        """Return outage heatmap data grouped by foreign source."""
        return self._get("heatmap/outages/foreignSources")

    def get_heatmap_outages_monitored_services(self):
        """Return outage heatmap data grouped by monitored service."""
        return self._get("heatmap/outages/monitoredServices")

    def get_heatmap_outages_nodes_by_category(self, category: str):
        """Return outage heatmap node data for *category*."""
        return self._get(f"heatmap/outages/nodesByCategory/{category}")

    def get_heatmap_outages_nodes_by_foreign_source(self, foreign_source: str):
        """Return outage heatmap node data for *foreign_source*."""
        return self._get(
            f"heatmap/outages/nodesByForeignSource/{foreign_source}")

    def get_heatmap_outages_nodes_by_service(self, service: str):
        """Return outage heatmap node data for monitored *service*."""
        return self._get(
            f"heatmap/outages/nodesByMonitoredService/{service}")

    # ==================================================================
    # Alarm-based heatmap
    # ==================================================================

    def get_heatmap_alarms_categories(self):
        """Return alarm heatmap data grouped by category."""
        return self._get("heatmap/alarms/categories")

    def get_heatmap_alarms_foreign_sources(self):
        """Return alarm heatmap data grouped by foreign source."""
        return self._get("heatmap/alarms/foreignSources")

    def get_heatmap_alarms_monitored_services(self):
        """Return alarm heatmap data grouped by monitored service."""
        return self._get("heatmap/alarms/monitoredServices")

    def get_heatmap_alarms_nodes_by_category(self, category: str):
        """Return alarm heatmap node data for *category*."""
        return self._get(f"heatmap/alarms/nodesByCategory/{category}")

    def get_heatmap_alarms_nodes_by_foreign_source(self, foreign_source: str):
        """Return alarm heatmap node data for *foreign_source*."""
        return self._get(
            f"heatmap/alarms/nodesByForeignSource/{foreign_source}")

    def get_heatmap_alarms_nodes_by_service(self, service: str):
        """Return alarm heatmap node data for monitored *service*."""
        return self._get(
            f"heatmap/alarms/nodesByMonitoredService/{service}")
