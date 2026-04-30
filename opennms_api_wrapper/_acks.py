from __future__ import annotations
"""Acknowledgements REST API – /rest/acks."""
from ._base import _OpenNMSBase
from typing import Any, Optional


class AcksMixin(_OpenNMSBase):
    def get_acks(self, limit: int = 10, offset: int = 0, **filters):
        """List acknowledgements.

        Args:
            limit: Max number of results to return. Use ``0`` for all.
            offset: Zero-based offset for pagination.
            **filters: Additional Hibernate query filters passed directly as query parameters (e.g. ``severity="MAJOR"``).
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        params.update(filters)
        return self._get("acks", params=params)

    def get_ack(self, ack_id: int):
        """Return the acknowledgement with the given ID."""
        return self._get(f"acks/{ack_id}")

    def get_ack_count(self) -> int:
        """Return the total number of acknowledgements."""
        return self._get("acks/count")

    # Write (form-encoded POST)

    def create_ack(self, action: str, alarm_id: Optional[int] = None,
                   notification_id: Optional[int] = None):
        """Create or modify an acknowledgement.

        Args:
            action: One of ``"ack"``, ``"unack"``, ``"clear"``, ``"esc"``.
            alarm_id: Target alarm ID (mutually exclusive with
                notification_id).
            notification_id: Target notification ID.
        """
        data: dict[str, Any] = {"action": action}
        if alarm_id is not None:
            data["alarmId"] = alarm_id
        if notification_id is not None:
            data["notifId"] = notification_id
        return self._post("acks", form_data=data)

    # Convenience wrappers

    def ack_notification(self, notification_id: int):
        """Acknowledge notification *notification_id*."""
        return self.create_ack("ack", notification_id=notification_id)

    def unack_notification(self, notification_id: int):
        """Remove acknowledgement from notification *notification_id*."""
        return self.create_ack("unack", notification_id=notification_id)
