"""Requisitions (Provisioning) REST API – /rest/requisitions."""


class RequisitionsMixin:
    # ==================================================================
    # Requisitions
    # ==================================================================

    def get_requisitions(self):
        """List all active (pending or deployed) requisitions."""
        return self._get("requisitions")

    def get_requisition(self, name: str):
        """Get a specific requisition by foreign source *name*."""
        return self._get(f"requisitions/{name}")

    def get_requisition_count(self) -> int:
        """Return the count of undeployed (pending) requisitions."""
        return self._get("requisitions/count")

    def get_deployed_requisitions(self):
        """List all deployed requisitions."""
        return self._get("requisitions/deployed")

    def get_deployed_requisition_count(self) -> int:
        """Return the count of deployed requisitions."""
        return self._get("requisitions/deployed/count")

    def create_requisition(self, requisition: dict):
        """Add or replace a requisition.

        Args:
            requisition: Requisition dict. Must contain at least
                ``{"foreign-source": "name", "node": []}``.
        """
        return self._post("requisitions", json_data=requisition)

    def import_requisition(self, name: str, rescan_existing: bool = True):
        """Synchronise/import requisition *name* into the database.

        Args:
            name: Foreign source name of the requisition to import.
            rescan_existing: When ``False`` only new/removed nodes are processed
                and existing nodes are not rescanned.
        """
        params = {} if rescan_existing else {"rescanExisting": "false"}
        return self._put(f"requisitions/{name}/import", params=params)

    def update_requisition(self, name: str, data: dict):
        """Update metadata on an existing requisition.

        Args:
            name: Foreign source name of the requisition.
            data: Dict of requisition fields to change.
        """
        return self._put(f"requisitions/{name}", json_data=data)

    def delete_requisition(self, name: str):
        """Delete a pending (not yet deployed) requisition."""
        return self._delete(f"requisitions/{name}")

    def delete_deployed_requisition(self, name: str):
        """Delete a deployed requisition."""
        return self._delete(f"requisitions/deployed/{name}")

    # ==================================================================
    # Requisition Nodes
    # ==================================================================

    def get_requisition_nodes(self, name: str):
        """List nodes in requisition *name*."""
        return self._get(f"requisitions/{name}/nodes")

    def get_requisition_node(self, name: str, foreign_id: str):
        """Get a specific node in a requisition by *foreign_id*."""
        return self._get(f"requisitions/{name}/nodes/{foreign_id}")

    def create_requisition_node(self, name: str, node: dict):
        """Add or replace a node in requisition *name*.

        Args:
            name: Foreign source name of the requisition.
            node: Node dict. Example::

                {
                    "foreign-id": "router01",
                    "node-label": "myrouter",
                    "location": "Default",
                    "interface": [
                        {
                            "ip-addr": "192.168.0.1",
                            "snmp-primary": "P",
                            "status": 1,
                            "monitored-service": [{"service-name": "ICMP"}]
                        }
                    ],
                    "category": [{"name": "Production"}],
                    "asset": [{"name": "description", "value": "Core router"}]
                }
        """
        return self._post(f"requisitions/{name}/nodes", json_data=node)

    def update_requisition_node(self, name: str, foreign_id: str, node: dict):
        """Update a node in requisition *name*.

        Args:
            name: Foreign source name of the requisition.
            foreign_id: Foreign ID of the node to update.
            node: Dict of node fields to change.
        """
        return self._put(f"requisitions/{name}/nodes/{foreign_id}",
                         json_data=node)

    def delete_requisition_node(self, name: str, foreign_id: str):
        """Delete a node from requisition *name* (async – returns 202)."""
        return self._delete(f"requisitions/{name}/nodes/{foreign_id}")

    # ==================================================================
    # Requisition Node Interfaces
    # ==================================================================

    def get_requisition_node_interfaces(self, name: str, foreign_id: str):
        """List interfaces for a node in a requisition."""
        return self._get(f"requisitions/{name}/nodes/{foreign_id}/interfaces")

    def create_requisition_node_interface(self, name: str, foreign_id: str,
                                          interface: dict):
        """Add or replace an interface on a requisition node.

        Args:
            name: Foreign source name of the requisition.
            foreign_id: Foreign ID of the node.
            interface: Interface dict with keys such as ``ip-addr``,
                ``snmp-primary``, ``status``, and ``monitored-service``.
        """
        return self._post(
            f"requisitions/{name}/nodes/{foreign_id}/interfaces",
            json_data=interface,
        )

    def update_requisition_node_interface(self, name: str, foreign_id: str,
                                          ip_address: str, interface: dict):
        """Update an interface on a requisition node.

        Args:
            name: Foreign source name of the requisition.
            foreign_id: Foreign ID of the node.
            ip_address: IP address of the interface to update.
            interface: Dict of interface fields to change.
        """
        return self._put(
            f"requisitions/{name}/nodes/{foreign_id}/interfaces/{ip_address}",
            json_data=interface,
        )

    def delete_requisition_node_interface(self, name: str, foreign_id: str,
                                          ip_address: str):
        """Delete an interface from a requisition node (async)."""
        return self._delete(
            f"requisitions/{name}/nodes/{foreign_id}/interfaces/{ip_address}")

    # ==================================================================
    # Requisition Node Interface Services
    # ==================================================================

    def get_requisition_node_services(self, name: str, foreign_id: str,
                                      ip_address: str):
        """List monitored services on a requisition node interface."""
        return self._get(
            f"requisitions/{name}/nodes/{foreign_id}/interfaces/{ip_address}/services")

    def create_requisition_node_service(self, name: str, foreign_id: str,
                                        ip_address: str, service: dict):
        """Add or replace a service on a requisition node interface.

        Args:
            name: Foreign source name of the requisition.
            foreign_id: Foreign ID of the node.
            ip_address: IP address of the interface.
            service: Service dict. Example: ``{"service-name": "HTTP"}``
        """
        return self._post(
            f"requisitions/{name}/nodes/{foreign_id}/interfaces/{ip_address}/services",
            json_data=service,
        )

    def delete_requisition_node_service(self, name: str, foreign_id: str,
                                        ip_address: str, service_name: str):
        """Delete a service from a requisition node interface (async)."""
        return self._delete(
            f"requisitions/{name}/nodes/{foreign_id}/interfaces"
            f"/{ip_address}/services/{service_name}"
        )

    # ==================================================================
    # Requisition Node Categories
    # ==================================================================

    def get_requisition_node_categories(self, name: str, foreign_id: str):
        """List categories for a requisition node."""
        return self._get(f"requisitions/{name}/nodes/{foreign_id}/categories")

    def add_requisition_node_category(self, name: str, foreign_id: str,
                                      category: dict):
        """Add or replace a category on a requisition node.

        Args:
            name: Foreign source name of the requisition.
            foreign_id: Foreign ID of the node.
            category: Category dict. Example: ``{"name": "Production"}``
        """
        return self._post(
            f"requisitions/{name}/nodes/{foreign_id}/categories",
            json_data=category,
        )

    def delete_requisition_node_category(self, name: str, foreign_id: str,
                                         category: str):
        """Delete a category from a requisition node (async)."""
        return self._delete(
            f"requisitions/{name}/nodes/{foreign_id}/categories/{category}")

    # ==================================================================
    # Requisition Node Assets
    # ==================================================================

    def get_requisition_node_assets(self, name: str, foreign_id: str):
        """List asset fields for a requisition node."""
        return self._get(f"requisitions/{name}/nodes/{foreign_id}/assets")

    def set_requisition_node_asset(self, name: str, foreign_id: str,
                                   asset: dict):
        """Add or replace an asset on a requisition node.

        Args:
            name: Foreign source name of the requisition.
            foreign_id: Foreign ID of the node.
            asset: Asset dict. Example: ``{"name": "serialNumber", "value": "SN-1234"}``
        """
        return self._post(
            f"requisitions/{name}/nodes/{foreign_id}/assets",
            json_data=asset,
        )

    def delete_requisition_node_asset(self, name: str, foreign_id: str,
                                      field: str):
        """Delete an asset field from a requisition node (async)."""
        return self._delete(
            f"requisitions/{name}/nodes/{foreign_id}/assets/{field}")
