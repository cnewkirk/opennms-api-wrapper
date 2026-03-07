"""SNMP Trap NBI Configuration REST API – /rest/config/snmptrap-nbi."""


class SnmpTrapNbiMixin:
    _SNMPTRAP_NBI = "config/snmptrap-nbi"

    def get_snmptrap_nbi_config(self):
        """Get the full SNMP trap NBI configuration."""
        return self._get(self._SNMPTRAP_NBI)

    def get_snmptrap_nbi_status(self):
        """Get the SNMP trap NBI forwarding status."""
        return self._get(f"{self._SNMPTRAP_NBI}/status")

    def set_snmptrap_nbi_status(self, enabled: bool):
        """Enable or disable SNMP trap NBI forwarding.

        Args:
            enabled: ``True`` to enable, ``False`` to disable.
        """
        return self._put(f"{self._SNMPTRAP_NBI}/status",
                         form_data={"enabled": str(enabled).lower()})

    def get_snmptrap_nbi_trapsinks(self):
        """List all SNMP trap NBI trap sinks."""
        return self._get(f"{self._SNMPTRAP_NBI}/trapsinks")

    def get_snmptrap_nbi_trapsink(self, name: str):
        """Get a specific trap sink by *name*."""
        return self._get(f"{self._SNMPTRAP_NBI}/trapsinks/{name}")

    def create_snmptrap_nbi_trapsink(self, data: dict):
        """Create a new SNMP trap NBI trap sink.

        Args:
            data: Trap sink definition dict with keys such as ``name``,
                ``ipAddress``, ``port``, ``community``.
        """
        return self._post(f"{self._SNMPTRAP_NBI}/trapsinks",
                          json_data=data)

    def update_snmptrap_nbi_trapsink(self, name: str, data: dict):
        """Update a trap sink.

        Args:
            name: Name of the trap sink to update.
            data: Form-encoded key/value pairs to update.
        """
        return self._put(f"{self._SNMPTRAP_NBI}/trapsinks/{name}",
                         form_data=data)

    def delete_snmptrap_nbi_trapsink(self, name: str):
        """Delete a trap sink."""
        return self._delete(f"{self._SNMPTRAP_NBI}/trapsinks/{name}")

    def update_snmptrap_nbi_config(self, data: dict):
        """Update the SNMP trap NBI configuration.

        Args:
            data: Updated configuration data dict.
        """
        return self._post(self._SNMPTRAP_NBI, json_data=data)
