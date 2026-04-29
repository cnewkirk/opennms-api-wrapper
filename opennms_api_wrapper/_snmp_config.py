"""SNMP Configuration REST API – /rest/snmpConfig."""
from ._base import _OpenNMSBase
from typing import Optional
from .types import SnmpConfig


class SnmpConfigMixin(_OpenNMSBase):
    def get_snmp_config(self, ip_address: str, location: Optional[str] = None):
        """Get the effective SNMP configuration for *ip_address*.

        Args:
            ip_address: Target IP address.
            location: Optional monitoring location name.
        """
        params = {}
        if location:
            params["location"] = location
        return self._get(f"snmpConfig/{ip_address}", params=params)

    def set_snmp_config(self, ip_address: str, config: SnmpConfig):
        """Add or update the SNMP configuration for *ip_address*.

        Args:
            ip_address: Target IP address.
            config: SNMP configuration.  See :class:`~opennms_api_wrapper.types.SnmpConfig`
                for all available fields.
        """
        return self._put(f"snmpConfig/{ip_address}", json_data=config)
