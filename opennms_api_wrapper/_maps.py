"""Maps REST API – /rest/maps.

Note:
    The maps REST API was removed upstream in OpenNMS Horizon 16
    (2015).  These methods are retained for backwards compatibility
    with pre-16 servers only and do not function on OpenNMS Horizon
    16+ or any Meridian release (the server responds 404).
"""
from ._base import _OpenNMSBase
from .types import Map


class MapsMixin(_OpenNMSBase):
    def get_maps(self):
        """List all maps.

        Note:
            Backwards compatibility only — the maps API was removed
            in OpenNMS Horizon 16 and this call 404s on newer servers.
        """
        return self._get("maps")

    def get_map(self, map_id: int):
        """Get a specific map by *map_id*.

        Note:
            Backwards compatibility only — the maps API was removed
            in OpenNMS Horizon 16 and this call 404s on newer servers.
        """
        return self._get(f"maps/{map_id}")

    def get_map_elements(self, map_id: int):
        """Get nodes, links, and elements for map *map_id*.

        Note:
            Backwards compatibility only — the maps API was removed
            in OpenNMS Horizon 16 and this call 404s on newer servers.
        """
        return self._get(f"maps/{map_id}/mapElements")

    def create_map(self, map_data: Map):
        """Add a new map.

        Note:
            Backwards compatibility only — the maps API was removed
            in OpenNMS Horizon 16 and this call 404s on newer servers.

        Args:
            map_data: Map definition dict.
        """
        return self._post("maps", json_data=map_data)

    def update_map(self, map_id: int, map_data: Map):
        """Update map properties.

        Note:
            Backwards compatibility only — the maps API was removed
            in OpenNMS Horizon 16 and this call 404s on newer servers.

        Args:
            map_id: Database ID of the map to update.
            map_data: Dict of map fields to change.
        """
        return self._put(f"maps/{map_id}", json_data=map_data)

    def delete_map(self, map_id: int):
        """Delete a map.

        Note:
            Backwards compatibility only — the maps API was removed
            in OpenNMS Horizon 16 and this call 404s on newer servers.
        """
        return self._delete(f"maps/{map_id}")
