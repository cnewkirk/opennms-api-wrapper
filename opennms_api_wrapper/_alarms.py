"""Alarms REST API – /rest/alarms and /api/v2/alarms."""


class AlarmsMixin:
    def get_alarms(self, limit: int = 10, offset: int = 0,
                   order_by: str = None, order: str = None, **filters):
        """List alarms (v1).

        Args:
            limit: Max number of results to return. Use ``0`` for all.
            offset: Zero-based offset for pagination.
            order_by: Field name to sort by.
            order: Sort direction: ``"asc"`` or ``"desc"``.
            **filters: Additional Hibernate query filters passed directly as
                query parameters (e.g. ``severity="MAJOR"``). Pass
                ``comparator`` to change the match type (eq/ilike/…).
        """
        params = {"limit": limit, "offset": offset}
        if order_by:
            params["orderBy"] = order_by
        if order:
            params["order"] = order
        params.update(filters)
        return self._get("alarms", params=params)

    def get_alarm(self, alarm_id: int):
        """Return the alarm with the given ID."""
        return self._get(f"alarms/{alarm_id}")

    def get_alarm_count(self) -> int:
        """Return the total number of alarms."""
        return self._get("alarms/count")

    # Single-alarm actions (v1 PUT with query params)

    def ack_alarm(self, alarm_id: int, ack_user: str = None):
        """Acknowledge alarm *alarm_id*.

        Args:
            ack_user: Acknowledge on behalf of this user (requires admin role).
        """
        params = {"ack": "true"}
        if ack_user:
            params["ackUser"] = ack_user
        return self._put(f"alarms/{alarm_id}", params=params)

    def unack_alarm(self, alarm_id: int):
        """Remove acknowledgement from alarm *alarm_id*."""
        return self._put(f"alarms/{alarm_id}", params={"ack": "false"})

    def clear_alarm(self, alarm_id: int):
        """Clear alarm *alarm_id* (sets severity to CLEARED)."""
        return self._put(f"alarms/{alarm_id}", params={"clear": "true"})

    def escalate_alarm(self, alarm_id: int):
        """Escalate the severity of alarm *alarm_id* by one step."""
        return self._put(f"alarms/{alarm_id}", params={"escalate": "true"})

    # Bulk alarm actions

    def bulk_ack_alarms(self, **filters):
        """Acknowledge all alarms matching the given filters.

        Args:
            **filters: Additional Hibernate query filters passed directly as query parameters (e.g. ``severity="MAJOR"``).
        """
        params = {"ack": "true"}
        params.update(filters)
        return self._put("alarms", params=params)

    def bulk_unack_alarms(self, **filters):
        """Remove acknowledgement from all alarms matching the given filters.

        Args:
            **filters: Additional Hibernate query filters passed directly as query parameters (e.g. ``severity="MAJOR"``).
        """
        params = {"ack": "false"}
        params.update(filters)
        return self._put("alarms", params=params)

    def bulk_clear_alarms(self, **filters):
        """Clear all alarms matching the given filters.

        Args:
            **filters: Additional Hibernate query filters passed directly as query parameters (e.g. ``severity="MAJOR"``).
        """
        params = {"clear": "true"}
        params.update(filters)
        return self._put("alarms", params=params)

    def bulk_escalate_alarms(self, **filters):
        """Escalate all alarms matching the given filters.

        Args:
            **filters: Additional Hibernate query filters passed directly as query parameters (e.g. ``severity="MAJOR"``).
        """
        params = {"escalate": "true"}
        params.update(filters)
        return self._put("alarms", params=params)

    # v2 alarms (FIQL filtering)

    def get_alarms_v2(self, fiql: str = None, limit: int = 10,
                      offset: int = 0, order_by: str = None,
                      order: str = None):
        """List alarms using the v2 API with optional FIQL filter string.

        Args:
            fiql: FIQL filter string (e.g. ``"alarm.severity==MAJOR"``).
            limit: Max number of results to return. Use ``0`` for all.
            offset: Zero-based offset for pagination.
            order_by: Field name to sort by.
            order: Sort direction: ``"asc"`` or ``"desc"``.

        Example::

            client.get_alarms_v2(fiql="alarm.severity==MAJOR")
        """
        params = {"limit": limit, "offset": offset}
        if fiql:
            params["_s"] = fiql
        if order_by:
            params["orderBy"] = order_by
        if order:
            params["order"] = order
        return self._get("alarms", params=params, v2=True)

    def get_alarm_v2(self, alarm_id: int):
        """Return a single alarm by ID using the v2 API."""
        return self._get(f"alarms/{alarm_id}", v2=True)
