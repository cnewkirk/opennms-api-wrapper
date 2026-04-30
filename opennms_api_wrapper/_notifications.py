from __future__ import annotations
"""Notifications REST API – /rest/notifications."""
from ._base import _OpenNMSBase
from typing import Any, Optional


class NotificationsMixin(_OpenNMSBase):
    def get_notifications(self, limit: int = 10, offset: int = 0,
                          order_by: Optional[str] = None, order: Optional[str] = None, **filters):
        """List notifications.

        Args:
            limit: Max number of results to return. Use ``0`` for all.
            offset: Zero-based offset for pagination.
            order_by: Field name to sort by.
            order: Sort direction: ``"asc"`` or ``"desc"``.
            **filters: Additional Hibernate query filters passed directly as query parameters (e.g. ``severity="MAJOR"``).
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if order_by:
            params["orderBy"] = order_by
        if order:
            params["order"] = order
        params.update(filters)
        return self._get("notifications", params=params)

    def get_notification(self, notification_id: int):
        """Get a single notification by ID."""
        return self._get(f"notifications/{notification_id}")

    def get_notification_count(self) -> int:
        """Return the total number of notifications."""
        return self._get("notifications/count")

    def trigger_destination_path(self, destination_path_name: str):
        """Trigger the targets of *destination_path_name* for testing."""
        return self._post(
            f"notifications/destination-paths/{destination_path_name}/trigger")
