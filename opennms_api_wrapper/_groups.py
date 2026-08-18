"""Groups REST API – /rest/groups."""
from xml.sax.saxutils import escape

from ._base import _OpenNMSBase
from .types import Group


class GroupsMixin(_OpenNMSBase):
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

        The body is sent as XML — ``POST /rest/groups`` does not
        accept JSON on any OpenNMS version.

        Args:
            group: Group definition dict. Keys: ``name`` (required),
                ``comments``, ``user`` (list of member usernames).
                Example:
                ``{"name": "network-ops", "comments": "Network operations team"}``
        """
        parts = [f"<name>{escape(str(group['name']))}</name>"]
        if "comments" in group:
            parts.append(
                f"<comments>{escape(str(group['comments']))}</comments>")
        for member in group.get("user", []):
            parts.append(f"<user>{escape(str(member))}</user>")
        xml = f"<group>{''.join(parts)}</group>"
        return self._post_text("groups", xml, "application/xml")

    def update_group(self, group_name: str, group: Group):
        """Update group metadata (e.g. comments field).

        The body is sent form-encoded — ``PUT /rest/groups/{name}``
        does not accept JSON on any OpenNMS version.

        Args:
            group_name: Name of the group to update.
            group: Dict of group fields to change,
                e.g. ``{"comments": "..."}``.
        """
        return self._put(f"groups/{group_name}", form_data=group)

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
