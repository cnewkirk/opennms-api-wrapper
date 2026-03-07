"""IP Interfaces REST API v2 – /api/v2/ipinterfaces (read-only)."""


class IpInterfacesV2Mixin:
    def get_ip_interfaces(self, fiql: str = None, limit: int = 10,
                          offset: int = 0):
        """List IP interfaces using the v2 API with optional FIQL filtering.

        This is a global (cross-node) read-only view.  For write operations
        use ``create_node_ip_interface()`` / ``delete_node_ip_interface()``.

        Args:
            fiql: FIQL filter string. Examples: ``"node.label==onms-prd-01"``,
                ``"ipAddress==192.168.32.140"``,
                ``"node.foreignSource==Servers"``.
            limit: Max number of results to return. Use ``0`` for all.
            offset: Zero-based offset for pagination.
        """
        params: dict = {"limit": limit, "offset": offset}
        if fiql:
            params["_s"] = fiql
        return self._get("ipinterfaces", params=params, v2=True)
