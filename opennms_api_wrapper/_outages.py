"""Outages REST API – /rest/outages (read-only)."""


class OutagesMixin:
    def get_outages(self, limit: int = 10, offset: int = 0, order_by: str = None,
                    order: str = None, **filters):
        """List outages (read-only).

        Args:
            limit: Max number of results to return. Use ``0`` for all.
            offset: Zero-based offset for pagination.
            order_by: Field name to sort by.
            order: Sort direction: ``"asc"`` or ``"desc"``.
            **filters: Additional Hibernate query filters passed directly as
                query parameters (e.g. ``node.label="myrouter"``).
        """
        params = {"limit": limit, "offset": offset}
        if order_by:
            params["orderBy"] = order_by
        if order:
            params["order"] = order
        params.update(filters)
        return self._get("outages", params=params)

    def get_outage(self, outage_id: int):
        """Get a single outage by ID."""
        return self._get(f"outages/{outage_id}")

    def get_outage_count(self) -> int:
        """Return the total number of outages."""
        return self._get("outages/count")

    def get_node_outages(self, node_id):
        """Get all outages for *node_id*."""
        return self._get(f"outages/forNode/{node_id}")
