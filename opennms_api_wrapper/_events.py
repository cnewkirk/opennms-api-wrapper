from __future__ import annotations
"""Events REST API – /rest/events."""
from ._base import _OpenNMSBase
from typing import Any, Optional
from .types import Event


class EventsMixin(_OpenNMSBase):
    def get_events(self, limit: int = 10, offset: int = 0,
                   order_by: Optional[str] = None, order: Optional[str] = None, **filters):
        """List events.

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
        return self._get("events", params=params)

    def get_event(self, event_id: int):
        """Return the event with the given ID."""
        return self._get(f"events/{event_id}")

    def get_event_count(self) -> int:
        """Return the total number of events."""
        return self._get("events/count")

    # Create

    def create_event(self, event: Event):
        """Publish an event to the OpenNMS event bus.

        Args:
            event: Event dict matching the OpenNMS event schema.

        Example:
            client.create_event({
                "uei": "uei.opennms.org/internal/test",
                "source": "my-script",
                "severity": "Normal",
                "nodeId": 1,
                "interface": "192.168.0.1",
                "parms": {
                    "parm": [
                        {"parmName": "key",
                         "value": {"content": "val"}}
                    ]
                }
            })
        """
        return self._post("events", json_data=event)

    def ack_event(self, event_id: int):
        """Acknowledge event *event_id*."""
        return self._put(f"events/{event_id}", params={"ack": "true"})

    def unack_event(self, event_id: int):
        """Remove acknowledgement from event *event_id*."""
        return self._put(f"events/{event_id}", params={"ack": "false"})

    def bulk_ack_events(self, **filters):
        """Acknowledge all events matching the given filters.

        Args:
            **filters: Additional Hibernate query filters passed directly as query parameters (e.g. ``severity="MAJOR"``).
        """
        params: dict[str, Any] = {"ack": "true"}
        params.update(filters)
        return self._put("events", params=params)

    def bulk_unack_events(self, **filters):
        """Remove acknowledgement from all events matching the given filters.

        Args:
            **filters: Additional Hibernate query filters passed directly as query parameters (e.g. ``severity="MAJOR"``).
        """
        params: dict[str, Any] = {"ack": "false"}
        params.update(filters)
        return self._put("events", params=params)
