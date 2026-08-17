"""Search REST API v2 – /api/v2/search."""
from ._base import _OpenNMSBase
from typing import Any, Optional


class SearchMixin(_OpenNMSBase):
    def search(self, query: str, context: Optional[str] = None,
               limit: Optional[int] = None):
        """Perform a global search across all search contexts.

        Results are grouped by context (e.g. ``Node``, ``Action``)
        and filtered by the requesting user's permissions.

        Args:
            query: Search query string.
            context: Optional context to restrict the search to.
                Searches all contexts when omitted.
            limit: Maximum results per context (default 10 on the
                server; negative for unbounded).

        Returns:
            List of search result groups, or ``None`` when nothing
            matched (204 No Content).
        """
        params: dict[str, Any] = {"_s": query}
        if context is not None:
            params["_c"] = context
        if limit is not None:
            params["_l"] = limit
        return self._get("search", params=params, v2=True)
