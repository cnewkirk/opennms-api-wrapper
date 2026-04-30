"""Alarm History REST API – /rest/alarms/history."""
from ._base import _OpenNMSBase
from typing import Optional


class AlarmHistoryMixin(_OpenNMSBase):
    def get_alarm_history(self, at: Optional[int] = None):
        """Return last known state of all active alarms.

        Args:
            at: Optional millisecond epoch timestamp for historical lookup.
        """
        params = {}
        if at is not None:
            params["at"] = at
        return self._get("alarms/history", params=params)

    def get_alarm_history_at(self, alarm_id: int, at: Optional[int] = None):
        """Return final known state of *alarm_id* (optionally at a point in time).

        Args:
            alarm_id: The alarm database ID.
            at: Optional millisecond epoch timestamp.
        """
        params = {}
        if at is not None:
            params["at"] = at
        return self._get(f"alarms/history/{alarm_id}", params=params)

    def get_alarm_history_states(self, alarm_id: int):
        """Return all state transitions for *alarm_id*."""
        return self._get(f"alarms/history/{alarm_id}/states")
