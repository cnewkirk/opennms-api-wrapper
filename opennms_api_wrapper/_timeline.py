"""Outage Timelines REST API – /rest/timeline."""
from ._base import _OpenNMSBase


class TimelineMixin(_OpenNMSBase):
    def get_timeline_header(self, start: int, end: int,
                            width: int) -> bytes:
        """Get the outage timeline header image.

        Args:
            start: Start of the timeline as an epoch timestamp
                (seconds).
            end: End of the timeline as an epoch timestamp (seconds).
            width: Width of the timeline in pixels.

        Returns:
            PNG image data.
        """
        return self._get_bytes(f"timeline/header/{start}/{end}/{width}")

    def get_timeline_image(self, node_id: int, ip_address: str,
                           service_id: int, start: int, end: int,
                           width: int) -> bytes:
        """Get the outage timeline image for a monitored service.

        Args:
            node_id: Node identifier.
            ip_address: IP address of the interface.
            service_id: Monitored service identifier.
            start: Start of the timeline as an epoch timestamp
                (seconds).
            end: End of the timeline as an epoch timestamp (seconds).
            width: Width of the timeline in pixels.

        Returns:
            PNG image data.
        """
        return self._get_bytes(
            f"timeline/image/{node_id}/{ip_address}/{service_id}"
            f"/{start}/{end}/{width}")

    def get_timeline_empty(self, start: int, end: int,
                           width: int) -> bytes:
        """Get an empty outage timeline image.

        Used for services that are not monitored.

        Args:
            start: Start of the timeline as an epoch timestamp
                (seconds).
            end: End of the timeline as an epoch timestamp (seconds).
            width: Width of the timeline in pixels.

        Returns:
            PNG image data.
        """
        return self._get_bytes(f"timeline/empty/{start}/{end}/{width}")

    def get_timeline_html(self, node_id: int, ip_address: str,
                          service_id: int, start: int, end: int,
                          width: int) -> str:
        """Get the raw HTML embedding the timeline image.

        Args:
            node_id: Node identifier.
            ip_address: IP address of the interface.
            service_id: Monitored service identifier.
            start: Start of the timeline as an epoch timestamp
                (seconds).
            end: End of the timeline as an epoch timestamp (seconds).
            width: Width of the timeline in pixels.
        """
        return self._get_text(
            f"timeline/html/{node_id}/{ip_address}/{service_id}"
            f"/{start}/{end}/{width}", accept="text/html")
