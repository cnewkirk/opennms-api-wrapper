"""Tests for SnmpMetadataMixin – /api/v2/snmpmetadata."""
import responses
from .conftest import V2
from .fixtures import SNMP_METADATA_ENTRY


@responses.activate
def test_get_snmp_metadata(client):
    responses.add(responses.GET, f"{V2}/snmpmetadata/1",
                  json=SNMP_METADATA_ENTRY)
    result = client.get_snmp_metadata(1)
    assert result["nodeId"] == 1
    assert result["entries"][0]["oid"] == ".1.3.6.1.2.1.1.1.0"
