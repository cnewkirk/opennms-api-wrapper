"""Monitored Services (ifservices) REST API – /rest/ifservices + v2."""
from ._base import _OpenNMSBase
from typing import Any, Optional


class IfServicesMixin(_OpenNMSBase):
    def get_ifservices(self, **kwargs):
        """List monitored services with optional query parameters.

        Args:
            **kwargs: Query parameters such as ``limit``, ``offset``,
                ``node.label``, ``ipInterface.ipAddress``, etc.
        """
        return self._get("ifservices", params=kwargs)

    def update_ifservices(self, **kwargs):
        """Bulk-update monitored services.

        Args:
            **kwargs: Form-encoded key/value pairs to update, e.g.
                ``status="A"`` plus filter parameters.
        """
        return self._put("ifservices", form_data=kwargs)

    def get_ifservices_v2(self, fiql: Optional[str] = None, limit: int = 10,
                          offset: int = 0):
        """List monitored services via the v2 API with FIQL filtering.

        Args:
            fiql: FIQL filter expression.
            limit: Maximum number of results.
            offset: Number of results to skip.
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if fiql:
            params["_s"] = fiql
        return self._get("ifservices", params=params, v2=True)
