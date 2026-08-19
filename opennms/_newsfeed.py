"""News Feed REST API v2 – /api/v2/newsfeed."""
from ._base import _OpenNMSBase


class NewsFeedMixin(_OpenNMSBase):
    def get_newsfeed(self):
        """Get the latest OpenNMS news feed items.

        Returns:
            Dict with news feed items including categories, tags,
            title, link, and descriptions.
        """
        return self._get("newsfeed", v2=True)
