"""SNMP Interfaces REST API v2 – /api/v2/snmpinterfaces (read-only)."""


class SnmpInterfacesV2Mixin:
    def get_snmp_interfaces(self, fiql: str = None, limit: int = 10,
                            offset: int = 0):
        """List SNMP interfaces using the v2 API with optional FIQL filtering.

        This is a global (cross-node) read-only view.  For write operations
        use ``create_node_snmp_interface()`` / ``delete_node_snmp_interface()``.

        Args:
            fiql: FIQL filter string. Examples: ``"node.label==onms-prd-01"``,
                ``"ifIndex==6"``,
                ``"node.foreignSource==Servers;ipInterfaces.ipAddress=127.0.0.1"``.
            limit: Max number of results to return. Use ``0`` for all.
            offset: Zero-based offset for pagination.
        """
        params: dict = {"limit": limit, "offset": offset}
        if fiql:
            params["_s"] = fiql
        return self._get("snmpinterfaces", params=params, v2=True)
