from __future__ import annotations
"""Nodes REST API – /rest/nodes and sub-resources."""
from ._base import _OpenNMSBase
from typing import Any, Optional
from .types import Node, NodeIpInterface, NodeSnmpInterface, NodeAssetRecord, HardwareEntity, Category


class NodesMixin(_OpenNMSBase):
    # ==================================================================
    # Nodes
    # ==================================================================

    def get_nodes(self, limit: int = 10, offset: int = 0, order_by: Optional[str] = None,
                  order: Optional[str] = None, **filters):
        """List nodes.

        Args:
            limit: Max number of results to return. Use ``0`` for all.
            offset: Zero-based offset for pagination.
            order_by: Field name to sort by.
            order: Sort direction: ``"asc"`` or ``"desc"``.
            **filters: Additional Hibernate query filters passed directly as
                query parameters (e.g. ``label="myrouter"``, ``category="Production"``).
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if order_by:
            params["orderBy"] = order_by
        if order:
            params["order"] = order
        params.update(filters)
        return self._get("nodes", params=params)

    def get_node(self, node_id):
        """Get a single node by database ID or ``"foreignSource:foreignId"``."""
        return self._get(f"nodes/{node_id}")

    def get_node_count(self) -> int:
        """Return the total number of nodes.

        Uses the v2 API because the v1 ``/nodes`` endpoint does not
        expose a ``/count`` sub-resource.
        """
        result = self._get("nodes", params={"limit": 1, "offset": 0},
                           v2=True)
        return result.get("totalCount", 0)

    def create_node(self, node: Node):
        """Create a node via the v1 API (POST /rest/nodes).

        Args:
            node: Node attribute dict. Common keys: ``label``, ``type``,
                ``foreignSource``, ``foreignId``, ``location``,
                ``sysContact``. Example::

                    {
                        "label": "myrouter",
                        "type": "A",
                        "foreignSource": "Routers",
                        "foreignId": "router01",
                        "location": "Default",
                        "sysContact": "ops@example.com",
                    }

        Note: The OpenNMS v1 nodes endpoint traditionally required XML.
        Modern Horizon releases (30+) accept JSON. If your server returns
        415, use the requisitions API instead (``create_requisition_node()``).
        """
        return self._post("nodes", json_data=node)

    def update_node(self, node_id, node: Node):
        """Update node properties (PUT /rest/nodes/{id}).

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            node: Dict of node fields to change.
        """
        return self._put(f"nodes/{node_id}", json_data=node)

    def delete_node(self, node_id):
        """Delete a node (async – returns 202 Accepted)."""
        return self._delete(f"nodes/{node_id}")

    def rescan_node(self, node_id):
        """Trigger a capability scan of *node_id* for new interfaces/services."""
        return self._post(f"nodes/{node_id}/rescan")

    # ==================================================================
    # IP Interfaces
    # ==================================================================

    def get_node_ip_interfaces(self, node_id, limit: int = 10, offset: int = 0,
                               **filters):
        """List IP interfaces for *node_id*.

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            limit: Max number of results to return. Use ``0`` for all.
            offset: Zero-based offset for pagination.
            **filters: Additional Hibernate query filters passed directly as query parameters (e.g. ``severity="MAJOR"``).
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        params.update(filters)
        return self._get(f"nodes/{node_id}/ipinterfaces", params=params)

    def get_node_ip_interface(self, node_id, ip_address: str):
        """Get a specific IP interface by *ip_address*."""
        return self._get(f"nodes/{node_id}/ipinterfaces/{ip_address}")

    def create_node_ip_interface(self, node_id, interface: NodeIpInterface):
        """Add an IP interface to *node_id*.

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            interface: Interface dict. Example::

                {"ipAddress": "192.168.0.1", "snmpPrimary": "P", "isManaged": "M"}
        """
        return self._post(f"nodes/{node_id}/ipinterfaces", json_data=interface)

    def update_node_ip_interface(self, node_id, ip_address: str, interface: NodeIpInterface):
        """Update an IP interface.

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            ip_address: IP address of the interface to update.
            interface: Dict of interface fields to change.
        """
        return self._put(f"nodes/{node_id}/ipinterfaces/{ip_address}",
                         json_data=interface)

    def delete_node_ip_interface(self, node_id, ip_address: str):
        """Delete an IP interface (async – returns 202 Accepted)."""
        return self._delete(f"nodes/{node_id}/ipinterfaces/{ip_address}")

    # ==================================================================
    # Monitored Services
    # ==================================================================

    def get_node_ip_services(self, node_id, ip_address: str):
        """List monitored services on *ip_address* of *node_id*."""
        return self._get(f"nodes/{node_id}/ipinterfaces/{ip_address}/services")

    def get_node_ip_service(self, node_id, ip_address: str, service: str):
        """Get a specific monitored service."""
        return self._get(
            f"nodes/{node_id}/ipinterfaces/{ip_address}/services/{service}")

    def create_node_ip_service(self, node_id, ip_address: str, service: dict):
        """Add a monitored service to *ip_address*.

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            ip_address: IP address of the interface.
            service: Service dict. Example: ``{"serviceType": {"name": "HTTP"}}``
        """
        return self._post(
            f"nodes/{node_id}/ipinterfaces/{ip_address}/services",
            json_data=service,
        )

    def delete_node_ip_service(self, node_id, ip_address: str, service: str):
        """Delete a monitored service (async – returns 202 Accepted)."""
        return self._delete(
            f"nodes/{node_id}/ipinterfaces/{ip_address}/services/{service}")

    # ==================================================================
    # SNMP Interfaces
    # ==================================================================

    def get_node_snmp_interfaces(self, node_id, limit: int = 10, offset: int = 0,
                                 **filters):
        """List SNMP interfaces for *node_id*.

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            limit: Max number of results to return. Use ``0`` for all.
            offset: Zero-based offset for pagination.
            **filters: Additional Hibernate query filters passed directly as query parameters (e.g. ``severity="MAJOR"``).
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        params.update(filters)
        return self._get(f"nodes/{node_id}/snmpinterfaces", params=params)

    def get_node_snmp_interface(self, node_id, ifindex: int):
        """Get a specific SNMP interface by ifIndex."""
        return self._get(f"nodes/{node_id}/snmpinterfaces/{ifindex}")

    def create_node_snmp_interface(self, node_id, interface: NodeSnmpInterface):
        """Add an SNMP interface to *node_id*.

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            interface: SNMP interface attribute dict.
        """
        return self._post(f"nodes/{node_id}/snmpinterfaces", json_data=interface)

    def update_node_snmp_interface(self, node_id, ifindex: int, interface: NodeSnmpInterface):
        """Update an SNMP interface.

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            ifindex: SNMP ifIndex of the interface to update.
            interface: Dict of interface fields to change.
        """
        return self._put(f"nodes/{node_id}/snmpinterfaces/{ifindex}",
                         json_data=interface)

    def delete_node_snmp_interface(self, node_id, ifindex: int):
        """Delete an SNMP interface (sync – returns 204)."""
        return self._delete(f"nodes/{node_id}/snmpinterfaces/{ifindex}")

    # ==================================================================
    # Categories
    # ==================================================================

    def get_node_categories(self, node_id):
        """List surveillance categories for *node_id*."""
        return self._get(f"nodes/{node_id}/categories")

    def get_node_category(self, node_id, category: str):
        """Get a specific category association for *node_id*."""
        return self._get(f"nodes/{node_id}/categories/{category}")

    def add_node_category(self, node_id, category: dict):
        """Add a category to *node_id*.

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            category: Category dict. Example: ``{"name": "Production"}``
        """
        return self._post(f"nodes/{node_id}/categories", json_data=category)

    def update_node_category(self, node_id, category: str, data: Category):
        """Update a category association for *node_id*.

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            category: Category name to update.
            data: Dict of category fields to change.
        """
        return self._put(f"nodes/{node_id}/categories/{category}", json_data=data)

    def delete_node_category(self, node_id, category: str):
        """Remove a category from *node_id* (sync – returns 204)."""
        return self._delete(f"nodes/{node_id}/categories/{category}")

    # ==================================================================
    # Asset Record
    # ==================================================================

    def get_node_asset_record(self, node_id):
        """Get the asset record for *node_id*."""
        return self._get(f"nodes/{node_id}/assetRecord")

    def update_node_asset_record(self, node_id, asset: NodeAssetRecord):
        """Update the asset record for *node_id*.

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            asset: Dict of asset fields to change. Common fields:
                ``description``, ``building``, ``floor``, ``room``, ``rack``,
                ``vendor``, ``modelNumber``, ``serialNumber``,
                ``operatingSystem``, etc.
        """
        return self._put(f"nodes/{node_id}/assetRecord", json_data=asset)

    # ==================================================================
    # Hardware Inventory
    # ==================================================================

    def get_node_hardware_inventory(self, node_id):
        """Get the hardware inventory tree for *node_id*."""
        return self._get(f"nodes/{node_id}/hardwareInventory")

    def get_node_hardware_entity(self, node_id, ent_physical_index: int):
        """Get a specific hardware entity by *ent_physical_index*."""
        return self._get(f"nodes/{node_id}/hardwareInventory/{ent_physical_index}")

    def add_node_hardware_inventory(self, node_id, data: HardwareEntity):
        """Add a hardware inventory entry to *node_id*.

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            data: Hardware inventory entity dict.
        """
        return self._post(f"nodes/{node_id}/hardwareInventory", json_data=data)

    def update_node_hardware_entity(self, node_id, ent_physical_index: int,
                                    data: HardwareEntity):
        """Update a specific hardware entity.

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            ent_physical_index: ENTITY-MIB entPhysicalIndex of the entity.
            data: Dict of entity fields to change.
        """
        return self._put(
            f"nodes/{node_id}/hardwareInventory/{ent_physical_index}",
            json_data=data,
        )

    def delete_node_hardware_entity(self, node_id, ent_physical_index: int):
        """Delete a specific hardware entity."""
        return self._delete(
            f"nodes/{node_id}/hardwareInventory/{ent_physical_index}")
