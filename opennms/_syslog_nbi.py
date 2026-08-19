"""Syslog NBI Configuration REST API – /rest/config/syslog-nbi."""
from ._base import _OpenNMSBase
from .types import SyslogNbiDestination, SyslogNbiConfig


class SyslogNbiMixin(_OpenNMSBase):
    _SYSLOG_NBI = "config/syslog-nbi"

    def get_syslog_nbi_config(self):
        """Get the full syslog NBI configuration."""
        return self._get(self._SYSLOG_NBI)

    def get_syslog_nbi_status(self):
        """Get the syslog NBI forwarding status."""
        return self._get(f"{self._SYSLOG_NBI}/status")

    def set_syslog_nbi_status(self, enabled: bool):
        """Enable or disable syslog NBI forwarding.

        Args:
            enabled: ``True`` to enable, ``False`` to disable.
        """
        return self._put(f"{self._SYSLOG_NBI}/status",
                         form_data={"enabled": str(enabled).lower()})

    def get_syslog_nbi_destinations(self):
        """List all syslog NBI destinations."""
        return self._get(f"{self._SYSLOG_NBI}/destinations")

    def get_syslog_nbi_destination(self, name: str):
        """Get a specific syslog destination by *name*."""
        return self._get(f"{self._SYSLOG_NBI}/destinations/{name}")

    def create_syslog_nbi_destination(self, data: SyslogNbiDestination):
        """Create a new syslog NBI destination.

        Args:
            data: Destination definition dict with keys such as ``name``,
                ``host``, ``port``, ``firstOccurrenceOnly``, ``filters``.
        """
        return self._post(f"{self._SYSLOG_NBI}/destinations",
                          json_data=data)

    def update_syslog_nbi_destination(self, name: str, data: SyslogNbiDestination):
        """Update a syslog NBI destination.

        Args:
            name: Name of the destination to update.
            data: Form-encoded key/value pairs to update.
        """
        return self._put(f"{self._SYSLOG_NBI}/destinations/{name}",
                         form_data=data)

    def delete_syslog_nbi_destination(self, name: str):
        """Delete a syslog NBI destination."""
        return self._delete(f"{self._SYSLOG_NBI}/destinations/{name}")

    def update_syslog_nbi_config(self, data: SyslogNbiConfig):
        """Update the syslog NBI configuration.

        Args:
            data: Updated configuration data dict.
        """
        return self._post(self._SYSLOG_NBI, json_data=data)
