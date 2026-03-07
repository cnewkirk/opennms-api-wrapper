"""SNMP Configuration REST API – /rest/snmpConfig."""


class SnmpConfigMixin:
    def get_snmp_config(self, ip_address: str, location: str = None):
        """Get the effective SNMP configuration for *ip_address*.

        Args:
            ip_address: Target IP address.
            location: Optional monitoring location name.
        """
        params = {}
        if location:
            params["location"] = location
        return self._get(f"snmpConfig/{ip_address}", params=params or None)

    def set_snmp_config(self, ip_address: str, config: dict):
        """Add or update the SNMP configuration for *ip_address*.

        Args:
            ip_address: Target IP address.
            config: SNMP configuration dict. Supports all ``<definition/>``
                attributes from ``snmp-config.xsd``. Common keys:
                ``version`` (``"v1"``, ``"v2c"``, ``"v3"``), ``community``,
                ``port``, ``timeout``, ``retries``. For SNMPv3:
                ``securityName``, ``authPassphrase``, ``authProtocol``
                (``"MD5"`` or ``"SHA"``), ``privPassphrase``,
                ``privProtocol`` (``"DES"``, ``"AES128"`` etc.),
                ``securityLevel`` (1=noAuth, 2=auth, 3=authPriv).
        """
        return self._put(f"snmpConfig/{ip_address}", json_data=config)
