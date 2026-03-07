"""Tests for SnmpInterfacesV2Mixin – /api/v2/snmpinterfaces (read-only)."""
import responses
from .conftest import V2, qs
from .fixtures import SNMP_INTERFACE_LIST


@responses.activate
def test_get_snmp_interfaces_defaults(client):
    responses.add(responses.GET, f"{V2}/snmpinterfaces",
                  json=SNMP_INTERFACE_LIST)
    result = client.get_snmp_interfaces()
    assert result["snmpInterface"][0]["ifIndex"] == 6
    assert result["snmpInterface"][0]["ifName"] == "GigabitEthernet0/0"
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["10"]
    assert params["offset"] == ["0"]
    assert "_s" not in params


@responses.activate
def test_get_snmp_interfaces_with_fiql(client):
    responses.add(responses.GET, f"{V2}/snmpinterfaces",
                  json=SNMP_INTERFACE_LIST)
    result = client.get_snmp_interfaces(fiql="ifIndex==6")
    assert result["snmpInterface"][0]["ifIndex"] == 6
    params = qs(responses.calls[0].request.url)
    assert params["_s"] == ["ifIndex==6"]


@responses.activate
def test_get_snmp_interfaces_pagination(client):
    responses.add(responses.GET, f"{V2}/snmpinterfaces",
                  json=SNMP_INTERFACE_LIST)
    client.get_snmp_interfaces(limit=50, offset=100)
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["50"]
    assert params["offset"] == ["100"]


@responses.activate
def test_get_snmp_interfaces_fiql_node_label(client):
    responses.add(responses.GET, f"{V2}/snmpinterfaces",
                  json=SNMP_INTERFACE_LIST)
    client.get_snmp_interfaces(fiql="node.label==onms-prd-01")
    params = qs(responses.calls[0].request.url)
    assert params["_s"] == ["node.label==onms-prd-01"]


@responses.activate
def test_get_snmp_interfaces_uses_v2_url(client):
    responses.add(responses.GET, f"{V2}/snmpinterfaces",
                  json=SNMP_INTERFACE_LIST)
    client.get_snmp_interfaces()
    assert "/api/v2/snmpinterfaces" in responses.calls[0].request.url
