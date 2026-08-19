"""User Defined Links REST API v2 – /api/v2/userdefinedlinks."""
from ._base import _OpenNMSBase
from .types import UserDefinedLink


class UserDefinedLinksMixin(_OpenNMSBase):
    def get_user_defined_links(self):
        """List all user-defined links."""
        return self._get("userdefinedlinks", v2=True)

    def get_user_defined_link(self, link_id: int):
        """Get a specific user-defined link by *link_id*."""
        return self._get(f"userdefinedlinks/{link_id}", v2=True)

    def create_user_defined_link(self, link: UserDefinedLink):
        """Create a new user-defined link.

        Args:
            link: Link definition dict with keys such as ``nodeIdA``,
                ``nodeIdZ``, ``componentLabelA``, ``componentLabelZ``,
                ``linkId``, ``linkLabel``, ``owner``.
        """
        return self._post("userdefinedlinks", json_data=link, v2=True)

    def delete_user_defined_link(self, link_id: int):
        """Delete a user-defined link."""
        return self._delete(f"userdefinedlinks/{link_id}", v2=True)
