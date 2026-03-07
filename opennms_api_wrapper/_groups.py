"""Groups REST API – /rest/groups."""
from .types import Group


class GroupsMixin:
    # ==================================================================
    # Groups
    # ==================================================================

    def get_groups(self):
        """List all user groups."""
        return self._get("groups")

    def get_group(self, group_name: str):
        """Get a specific group by *group_name*."""
        return self._get(f"groups/{group_name}")

    def create_group(self, group: Group):
        """Create a new user group.

        Args:
            group: Group definition dict. Example:
                ``{"name": "network-ops", "comments": "Network operations team"}``
        """
        return self._post("groups", json_data=group)

    def update_group(self, group_name: str, group: Group):
        """Update group metadata (e.g. comments field).

        Args:
            group_name: Name of the group to update.
            group: Dict of group fields to change.
        """
        return self._put(f"groups/{group_name}", json_data=group)

    def delete_group(self, group_name: str):
        """Delete a user group."""
        return self._delete(f"groups/{group_name}")

    # ==================================================================
    # Group Members
    # ==================================================================

    def get_group_users(self, group_name: str):
        """List users in *group_name*."""
        return self._get(f"groups/{group_name}/users")

    def add_user_to_group(self, group_name: str, username: str):
        """Add *username* to *group_name*."""
        return self._put(f"groups/{group_name}/users/{username}")

    def remove_user_from_group(self, group_name: str, username: str):
        """Remove *username* from *group_name*."""
        return self._delete(f"groups/{group_name}/users/{username}")

    # ==================================================================
    # Group Categories
    # ==================================================================

    def get_group_categories(self, group_name: str):
        """List surveillance categories associated with *group_name*."""
        return self._get(f"groups/{group_name}/categories")

    def add_category_to_group(self, group_name: str, category_name: str):
        """Associate *category_name* with *group_name*."""
        return self._put(f"groups/{group_name}/categories/{category_name}")

    def remove_category_from_group(self, group_name: str, category_name: str):
        """Remove *category_name* from *group_name*."""
        return self._delete(f"groups/{group_name}/categories/{category_name}")
