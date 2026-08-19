"""Grafana Endpoints REST API – /rest/endpoints/grafana."""
from ._base import _OpenNMSBase
from .types import GrafanaEndpoint


class GrafanaEndpointsMixin(_OpenNMSBase):
    def get_grafana_endpoints(self):
        """Get all configured Grafana endpoints.

        Returns:
            List of endpoint definitions, or ``None`` when none are
            configured (204 No Content).
        """
        return self._get("endpoints/grafana")

    def get_grafana_endpoint(self, endpoint_id: int):
        """Get a Grafana endpoint by its numeric identifier.

        Args:
            endpoint_id: Numeric endpoint identifier.
        """
        return self._get(f"endpoints/grafana/{endpoint_id}")

    def get_grafana_dashboards(self, uid: str):
        """Get the dashboards of the Grafana endpoint with *uid*.

        Args:
            uid: Unique identifier of the Grafana endpoint.
        """
        return self._get(f"endpoints/grafana/{uid}/dashboards")

    def get_grafana_dashboard(self, uid: str, dashboard_id: str):
        """Get a dashboard from the Grafana endpoint with *uid*.

        Args:
            uid: Unique identifier of the Grafana endpoint.
            dashboard_id: Identifier of the dashboard to fetch.
        """
        return self._get(
            f"endpoints/grafana/{uid}/dashboards/{dashboard_id}")

    def create_grafana_endpoint(self, endpoint: GrafanaEndpoint):
        """Create a new Grafana endpoint.

        Args:
            endpoint: Endpoint definition; ``uid``, ``url``, and
                ``apiKey`` are required.
        """
        return self._post("endpoints/grafana", json_data=endpoint)

    def verify_grafana_endpoint(self, endpoint: GrafanaEndpoint):
        """Verify connectivity of a Grafana endpoint definition.

        Args:
            endpoint: Endpoint definition to verify (``url`` and
                ``apiKey`` at minimum).
        """
        return self._post("endpoints/grafana/verify",
                          json_data=endpoint)

    def update_grafana_endpoint(self, endpoint_id: int,
                                endpoint: GrafanaEndpoint):
        """Update an existing Grafana endpoint.

        Args:
            endpoint_id: Numeric endpoint identifier.
            endpoint: Updated endpoint definition (must include
                ``id``).
        """
        return self._put(f"endpoints/grafana/{endpoint_id}",
                         json_data=endpoint)

    def delete_grafana_endpoints(self):
        """Delete all Grafana endpoints."""
        return self._delete("endpoints/grafana")

    def delete_grafana_endpoint(self, endpoint_id: int):
        """Delete a Grafana endpoint by its numeric identifier.

        Args:
            endpoint_id: Numeric endpoint identifier.
        """
        return self._delete(f"endpoints/grafana/{endpoint_id}")
