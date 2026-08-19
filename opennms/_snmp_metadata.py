"""SNMP Metadata REST API v2 – /api/v2/snmpmetadata."""
from ._base import _OpenNMSBase


class SnmpMetadataMixin(_OpenNMSBase):
    def get_snmp_metadata(self, node_id: int):
        """Get SNMP metadata collected for a node.

        Args:
            node_id: Node database ID.
        """
        return self._get(f"snmpmetadata/{node_id}", v2=True)
