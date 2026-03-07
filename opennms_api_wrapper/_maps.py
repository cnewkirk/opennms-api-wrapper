"""Maps REST API – /rest/maps."""
from .types import Map


class MapsMixin:
    def get_maps(self):
        """List all maps."""
        return self._get("maps")

    def get_map(self, map_id: int):
        """Get a specific map by *map_id*."""
        return self._get(f"maps/{map_id}")

    def get_map_elements(self, map_id: int):
        """Get nodes, links, and elements for map *map_id*."""
        return self._get(f"maps/{map_id}/mapElements")

    def create_map(self, map_data: Map):
        """Add a new map.

        Args:
            map_data: Map definition dict.
        """
        return self._post("maps", json_data=map_data)

    def update_map(self, map_id: int, map_data: Map):
        """Update map properties.

        Args:
            map_id: Database ID of the map to update.
            map_data: Dict of map fields to change.
        """
        return self._put(f"maps/{map_id}", json_data=map_data)

    def delete_map(self, map_id: int):
        """Delete a map."""
        return self._delete(f"maps/{map_id}")
