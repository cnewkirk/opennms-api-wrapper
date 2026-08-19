"""Status REST API v2 – /api/v2/status."""
from __future__ import annotations
from ._base import _OpenNMSBase
from typing import Any, Optional


class StatusMixin(_OpenNMSBase):
    def _status_list_params(self, limit, offset, order_by, order,
                            severity_filter):
        """Build the shared query parameters for status list calls."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if order_by is not None:
            params["orderBy"] = order_by
        if order is not None:
            params["order"] = order
        if severity_filter is not None:
            params["severityFilter"] = severity_filter
        return params or None

    def get_status_summary_nodes(self, type: str = "alarms"):
        """Get a severity-count summary of nodes.

        Args:
            type: Status computation strategy — ``"alarms"`` or
                ``"outages"``.

        Returns:
            List of ``[severity_label, count]`` pairs.
        """
        return self._get(f"status/summary/nodes/{type}", v2=True)

    def get_status_summary_applications(self):
        """Get a severity-count summary of all applications.

        Returns:
            List of ``[severity_label, count]`` pairs.
        """
        return self._get("status/summary/applications", v2=True)

    def get_status_summary_business_services(self):
        """Get a severity-count summary of all business services.

        Returns:
            List of ``[severity_label, count]`` pairs.
        """
        return self._get("status/summary/business-services", v2=True)

    def get_status_nodes(self, type: str = "alarms",
                         limit: Optional[int] = None,
                         offset: Optional[int] = None,
                         order_by: Optional[str] = None,
                         order: Optional[str] = None,
                         severity_filter: Optional[str] = None):
        """Get nodes with their computed status.

        Args:
            type: Status computation strategy — ``"alarms"`` or
                ``"outages"``.
            limit: Maximum number of results.
            offset: Result offset for pagination.
            order_by: Property to order by.
            order: Sort order, ``"asc"`` or ``"desc"``.
            severity_filter: Only return entries with this severity.
        """
        params = self._status_list_params(limit, offset, order_by,
                                          order, severity_filter)
        return self._get(f"status/nodes/{type}", params=params, v2=True)

    def get_status_applications(self, limit: Optional[int] = None,
                                offset: Optional[int] = None,
                                order_by: Optional[str] = None,
                                order: Optional[str] = None,
                                severity_filter: Optional[str] = None):
        """Get applications with their computed status.

        Args:
            limit: Maximum number of results.
            offset: Result offset for pagination.
            order_by: Property to order by.
            order: Sort order, ``"asc"`` or ``"desc"``.
            severity_filter: Only return entries with this severity.
        """
        params = self._status_list_params(limit, offset, order_by,
                                          order, severity_filter)
        return self._get("status/applications", params=params, v2=True)

    def get_status_business_services(self, limit: Optional[int] = None,
                                     offset: Optional[int] = None,
                                     order_by: Optional[str] = None,
                                     order: Optional[str] = None,
                                     severity_filter: Optional[str] = None):
        """Get business services with their computed status.

        Args:
            limit: Maximum number of results.
            offset: Result offset for pagination.
            order_by: Property to order by.
            order: Sort order, ``"asc"`` or ``"desc"``.
            severity_filter: Only return entries with this severity.
        """
        params = self._status_list_params(limit, offset, order_by,
                                          order, severity_filter)
        return self._get("status/business-services", params=params,
                         v2=True)
