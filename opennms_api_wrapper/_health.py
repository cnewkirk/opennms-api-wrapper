"""Health REST API – /rest/health."""


class HealthMixin:
    def get_health(self, tag: str = None):
        """Get the health status of the OpenNMS instance.

        Args:
            tag: Optional tag to filter health checks.
        """
        params = {"tag": tag} if tag else None
        return self._get("health", params=params)

    def get_health_probe(self):
        """Get a simple health probe (up/down) response."""
        return self._get("health/probe")
