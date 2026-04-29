"""Minions REST API – /rest/minions."""
from ._base import _OpenNMSBase


class MinionsMixin(_OpenNMSBase):
    def get_minions(self, limit: int = 10, offset: int = 0):
        """List all minions.

        Args:
            limit: Maximum number of results. Use ``0`` for all.
            offset: Number of results to skip (for pagination).
        """
        params = {"limit": limit, "offset": offset}
        return self._get("minions", params=params)

    def get_minion(self, minion_id: str):
        """Get a specific minion by *minion_id*."""
        return self._get(f"minions/{minion_id}")

    def get_minion_count(self):
        """Return the number of minions."""
        return self._get("minions/count")
