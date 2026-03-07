"""Business Service Monitoring REST API v2 – /api/v2/business-services."""


class BusinessServicesMixin:
    def get_business_services(self):
        """List all business services."""
        return self._get("business-services", v2=True)

    def get_business_service(self, service_id: int):
        """Get a specific business service by *service_id*."""
        return self._get(f"business-services/{service_id}", v2=True)

    def create_business_service(self, service: dict):
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

    def update_business_service(self, service_id: int, service: dict):
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
