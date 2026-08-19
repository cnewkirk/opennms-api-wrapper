"""Situations REST API v2 – /api/v2/situations."""
from ._base import _OpenNMSBase
from typing import Optional


class SituationsMixin(_OpenNMSBase):
    def get_situations(self, limit: int = 10, offset: int = 0):
        """List situations (v2).

        Args:
            limit: Max number of results to return. Use ``0`` for all.
            offset: Zero-based offset for pagination.
        """
        return self._get("situations", params={"limit": limit, "offset": offset},
                         v2=True)

    def create_situation(self, alarm_ids: list, description: Optional[str] = None,
                         diagnostic_text: Optional[str] = None):
        """Create a new situation from a list of alarm IDs.

        Args:
            alarm_ids: List of integer alarm IDs.
            description: Optional situation description.
            diagnostic_text: Optional diagnostic text.
        """
        body: dict = {"alarmIdList": ",".join(str(i) for i in alarm_ids)}
        if description is not None:
            body["description"] = description
        if diagnostic_text is not None:
            body["diagnosticText"] = diagnostic_text
        return self._post("situations/create", json_data=body, v2=True)

    def add_alarms_to_situation(self, situation_id: int, alarm_ids: list,
                                feedback: Optional[str] = None):
        """Link additional alarm IDs to an existing situation.

        Args:
            situation_id: Target situation ID.
            alarm_ids: List of integer alarm IDs to associate.
            feedback: Optional feedback string.
        """
        body: dict = {
            "situationId": situation_id,
            "alarmIdList": ",".join(str(i) for i in alarm_ids),
        }
        if feedback is not None:
            body["feedback"] = feedback
        return self._post("situations/associateAlarm", json_data=body, v2=True)

    def clear_situation(self, situation_id: int):
        """Clear a situation by ID."""
        return self._post("situations/clear",
                          json_data={"situationId": situation_id}, v2=True)

    def clear_situation_alarms(self, situation_id: int, alarm_ids: list):
        """Remove *alarm_ids* from a situation and clear them.

        Args:
            situation_id: Target situation ID.
            alarm_ids: List of integer alarm IDs to remove and clear.
        """
        body = {
            "situationId": situation_id,
            "alarmIdList": ",".join(str(i) for i in alarm_ids),
        }
        return self._post("situations/alarms/clear", json_data=body, v2=True)

    def accept_situation(self, situation_id: int):
        """Accept (acknowledge) a situation."""
        return self._post(f"situations/accepted/{situation_id}", v2=True)

    def remove_alarms_from_situation(self, situation_id: int, alarm_ids: list):
        """Remove specific alarm IDs from a situation without clearing them.

        Args:
            situation_id: Target situation ID.
            alarm_ids: List of integer alarm IDs to remove.
        """
        body = {
            "situationId": situation_id,
            "alarmIdList": ",".join(str(i) for i in alarm_ids),
        }
        return self._delete("situations/removeAlarm", params=body, v2=True)
