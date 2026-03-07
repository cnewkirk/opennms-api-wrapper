"""Business Service Monitoring REST API v2 – /api/v2/business-services."""
from .types import BusinessService, BsIpServiceEdge, BsReductionKeyEdge, BsChildEdge


class BusinessServicesMixin:
    def get_business_services(self):
        """List all business services."""
        return self._get("business-services", v2=True)

    def get_business_service(self, service_id: int):
        """Get a specific business service by *service_id*."""
        return self._get(f"business-services/{service_id}", v2=True)

    def create_business_service(self, service: BusinessService):
        """Create a new business service.

        Args:
            service: Business service definition dict. Common keys:
                ``name`` (str), ``attributes`` (dict of key/value pairs),
                ``reduceFunction`` (dict with a ``type`` key),
                ``edges`` (list of edge configuration dicts). Example::

                    {
                        "name": "My App",
                        "attributes": {"dc": "us-east-1"},
                        "reduceFunction": {"type": "HighestSeverity"},
                    }
        """
        return self._post("business-services", json_data=service, v2=True)

    def update_business_service(self, service_id: int, service: BusinessService):
        """Update a business service.

        Args:
            service_id: Database ID of the business service to update.
            service: Updated business service definition dict.
        """
        return self._put(f"business-services/{service_id}", json_data=service,
                         v2=True)

    def delete_business_service(self, service_id: int):
        """Delete a business service."""
        return self._delete(f"business-services/{service_id}", v2=True)

    # ------------------------------------------------------------------
    # Edges
    # ------------------------------------------------------------------

    def get_business_service_edge(self, edge_id: int):
        """Get a specific business service edge by *edge_id*."""
        return self._get(f"business-services/edges/{edge_id}", v2=True)

    def add_ip_service_edge(self, service_id: int, edge: BsIpServiceEdge):
        """Add an IP-service edge to a business service.

        Args:
            service_id: Database ID of the business service.
            edge: Edge definition dict with keys such as ``ipServiceId``,
                ``mapFunction``, and ``weight``.
        """
        return self._post(
            f"business-services/{service_id}/ip-service-edge",
            json_data=edge, v2=True)

    def add_reduction_key_edge(self, service_id: int, edge: BsReductionKeyEdge):
        """Add a reduction-key edge to a business service.

        Args:
            service_id: Database ID of the business service.
            edge: Edge definition dict with keys such as ``reductionKey``,
                ``mapFunction``, and ``weight``.
        """
        return self._post(
            f"business-services/{service_id}/reduction-key-edge",
            json_data=edge, v2=True)

    def add_child_edge(self, service_id: int, edge: BsChildEdge):
        """Add a child-service edge to a business service.

        Args:
            service_id: Database ID of the business service.
            edge: Edge definition dict with keys such as ``childId``,
                ``mapFunction``, and ``weight``.
        """
        return self._post(
            f"business-services/{service_id}/child-edge",
            json_data=edge, v2=True)

    def remove_business_service_edge(self, service_id: int, edge_id: int):
        """Remove an edge from a business service.

        Args:
            service_id: Database ID of the business service.
            edge_id: Database ID of the edge to remove.
        """
        return self._delete(
            f"business-services/{service_id}/edges/{edge_id}", v2=True)

    # ------------------------------------------------------------------
    # Daemon
    # ------------------------------------------------------------------

    def reload_business_service_daemon(self):
        """Reload the Business Service Monitoring daemon."""
        return self._post("business-services/daemon/reload", v2=True)

    # ------------------------------------------------------------------
    # Functions
    # ------------------------------------------------------------------

    def get_map_functions(self):
        """List all available map functions."""
        return self._get("business-services/functions/map", v2=True)

    def get_map_function(self, name: str):
        """Get a specific map function by *name*."""
        return self._get(f"business-services/functions/map/{name}",
                         v2=True)

    def get_reduce_functions(self):
        """List all available reduce functions."""
        return self._get("business-services/functions/reduce", v2=True)

    def get_reduce_function(self, name: str):
        """Get a specific reduce function by *name*."""
        return self._get(f"business-services/functions/reduce/{name}",
                         v2=True)
