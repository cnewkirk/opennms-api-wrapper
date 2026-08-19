"""Situation Feedback REST API – /rest/situation-feedback."""
from ._base import _OpenNMSBase
from typing import Optional


class SituationFeedbackMixin(_OpenNMSBase):
    def get_situation_feedback_tags(self, prefix: Optional[str] = None):
        """List situation feedback tags.

        Args:
            prefix: Optional prefix to filter tags.
        """
        params = {"prefix": prefix} if prefix else None
        return self._get("situation-feedback/tags", params=params)

    def get_situation_feedback(self, situation_id: int):
        """Get feedback for a specific situation.

        Args:
            situation_id: Alarm ID of the situation.
        """
        return self._get(f"situation-feedback/{situation_id}")

    def submit_situation_feedback(self, situation_id: int,
                                  feedback: list):
        """Submit feedback for a situation.

        Args:
            situation_id: Alarm ID of the situation.
            feedback: List of feedback entry dicts, each with keys such
                as ``alarmKey``, ``fingerprint``, ``feedbackType``,
                ``reason``, ``user``, ``timestamp``.
        """
        return self._post(f"situation-feedback/{situation_id}",
                          json_data=feedback)
