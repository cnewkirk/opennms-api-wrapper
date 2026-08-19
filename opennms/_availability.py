"""Availability REST API – /rest/availability."""
from ._base import _OpenNMSBase


class AvailabilityMixin(_OpenNMSBase):
    def get_availability(self):
        """Get availability summary for all categories."""
        return self._get("availability")

    def get_availability_category(self, category: str):
        """Get availability summary for a specific *category*.

        Args:
            category: Surveillance category name.
        """
        return self._get(f"availability/categories/{category}")

    def get_availability_category_nodes(self, category: str):
        """Get per-node availability for a specific *category*.

        Args:
            category: Surveillance category name.
        """
        return self._get(f"availability/categories/{category}/nodes")

    def get_availability_category_node(self, category: str,
                                       node_id: int):
        """Get availability for a specific node within a *category*.

        Args:
            category: Surveillance category name.
            node_id: Node database ID.
        """
        return self._get(
            f"availability/categories/{category}/nodes/{node_id}")

    def get_availability_node(self, node_id: int):
        """Get availability summary for a specific node.

        Args:
            node_id: Node database ID.
        """
        return self._get(f"availability/nodes/{node_id}")
