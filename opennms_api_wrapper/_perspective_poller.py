"""Perspective Poller REST API v2 – /api/v2/perspectivepoller."""
from ._base import _OpenNMSBase
from typing import Optional


class PerspectivePollerMixin(_OpenNMSBase):
    def get_perspective_poller_status(self, app_id: int,
                                     start: Optional[int] = None,
                                     end: Optional[int] = None):
        """Get perspective poller status for an application.

        Args:
            app_id: Application database ID.
            start: Optional start time in ms since epoch.
            end: Optional end time in ms since epoch.
        """
        params = {}
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        return self._get(f"perspectivepoller/{app_id}",
                         params=params, v2=True)

    def get_perspective_poller_service_status(self, app_id: int,
                                             service_id: int,
                                             start: Optional[int] = None,
                                             end: Optional[int] = None):
        """Get perspective poller status for a specific service.

        Args:
            app_id: Application database ID.
            service_id: Monitored service database ID.
            start: Optional start time in ms since epoch.
            end: Optional end time in ms since epoch.
        """
        params = {}
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        return self._get(
            f"perspectivepoller/{app_id}/{service_id}",
            params=params, v2=True)
