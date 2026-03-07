"""Event Configuration REST API v2 – /api/v2/eventconf."""
from .types import EventConfEvent


class EventConfMixin:
    # ------------------------------------------------------------------
    # Filter
    # ------------------------------------------------------------------

    def get_eventconf_filter(self, uei: str = None, vendor: str = None,
                             **kwargs):
        """Get event configuration with optional filtering.

        Args:
            uei: Optional UEI pattern to filter by.
            vendor: Optional vendor name to filter by.
            **kwargs: Additional query parameters.
        """
        params = dict(kwargs)
        if uei:
            params["uei"] = uei
        if vendor:
            params["vendor"] = vendor
        return self._get("eventconf/filter", params=params,
                         v2=True)

    def get_eventconf_filter_sources(self, filter: str = None,
                                     **kwargs):
        """Get event configuration sources.

        Args:
            filter: Optional filter expression.
            **kwargs: Additional query parameters.
        """
        params = dict(kwargs)
        if filter:
            params["filter"] = filter
        return self._get("eventconf/filter/sources",
                         params=params, v2=True)

    def get_eventconf_filter_events(self, source_id: str, **kwargs):
        """Get events for a specific configuration source.

        Args:
            source_id: Event configuration source identifier.
            **kwargs: Additional query parameters.
        """
        return self._get(f"eventconf/filter/{source_id}/events",
                         params=kwargs, v2=True)

    # ------------------------------------------------------------------
    # Sources
    # ------------------------------------------------------------------

    def get_eventconf_source_names(self):
        """List all event configuration source names."""
        return self._get("eventconf/sources/names", v2=True)

    def get_eventconf_source(self, source_id: str):
        """Get a specific event configuration source.

        Args:
            source_id: Event configuration source identifier.
        """
        return self._get(f"eventconf/sources/{source_id}", v2=True)

    def download_eventconf_events(self, source_id: str):
        """Download events for a source as raw XML text.

        Args:
            source_id: Event configuration source identifier.

        Returns:
            Raw response text (typically XML).
        """
        return self._get_text(
            f"eventconf/sources/{source_id}/events/download", v2=True)

    # ------------------------------------------------------------------
    # Vendor events
    # ------------------------------------------------------------------

    def get_eventconf_vendor_events(self, vendor_name: str):
        """Get events for a specific vendor.

        Args:
            vendor_name: Vendor name.
        """
        return self._get(f"eventconf/vendors/{vendor_name}/events",
                         v2=True)

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def create_eventconf_event(self, source_id: str, event: EventConfEvent):
        """Create a new event definition in a source.

        Args:
            source_id: Event configuration source identifier.
            event: Event definition dict.
        """
        return self._post(
            f"eventconf/sources/{source_id}/events",
            json_data=event, v2=True)

    def update_eventconf_event(self, source_id: str, event_id: str,
                               event: EventConfEvent):
        """Update an event definition.

        Args:
            source_id: Event configuration source identifier.
            event_id: Event identifier within the source.
            event: Updated event definition dict.
        """
        return self._put(
            f"eventconf/sources/{source_id}/events/{event_id}",
            json_data=event, v2=True)

    # ------------------------------------------------------------------
    # Upload
    # ------------------------------------------------------------------

    def upload_eventconf(self, file_path_or_bytes):
        """Upload an event configuration file.

        Args:
            file_path_or_bytes: Either a file path (str) or raw bytes
                to upload as multipart form data.
        """
        if isinstance(file_path_or_bytes, str):
            with open(file_path_or_bytes, "rb") as fh:
                return self._post_files(
                    "eventconf/upload", files={"file": fh},
                    v2=True)
        files = {"file": ("events.xml", file_path_or_bytes)}
        return self._post_files("eventconf/upload", files=files,
                                v2=True)

    # ------------------------------------------------------------------
    # Status (PATCH)
    # ------------------------------------------------------------------

    def set_eventconf_sources_status(self, payload: dict):
        """Set the enabled/disabled status of event configuration sources.

        Args:
            payload: Dict mapping source IDs to boolean status values.
        """
        return self._patch("eventconf/sources/status",
                           json_data=payload, v2=True)

    def set_eventconf_events_status(self, source_id: str,
                                    payload: dict):
        """Set the enabled/disabled status of events within a source.

        Args:
            source_id: Event configuration source identifier.
            payload: Dict mapping event IDs to boolean status values.
        """
        return self._patch(
            f"eventconf/sources/{source_id}/events/status",
            json_data=payload, v2=True)

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    def delete_eventconf_sources(self, payload: dict):
        """Delete event configuration sources.

        Args:
            payload: Dict or list identifying sources to delete.
        """
        return self._delete("eventconf/sources", json_data=payload,
                            v2=True)

    def delete_eventconf_events(self, source_id: str, payload: dict):
        """Delete events from a source.

        Args:
            source_id: Event configuration source identifier.
            payload: Dict or list identifying events to delete.
        """
        return self._delete(
            f"eventconf/sources/{source_id}/events",
            json_data=payload, v2=True)
