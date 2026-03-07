"""Tests for SnmpConfigMixin – /rest/snmpConfig."""
import json
import responses
from .conftest import V1, qs
from .fixtures import SNMP_CONFIG


@responses.activate
def test_get_snmp_config(client):
    responses.add(responses.GET, f"{V1}/snmpConfig/192.168.1.1",
                  json=SNMP_CONFIG)
    result = client.get_snmp_config("192.168.1.1")
    assert result["version"] == "v2c"
    assert result["community"] == "public"
    assert result["port"] == 161


@responses.activate
def test_get_snmp_config_with_location(client):
    responses.add(responses.GET, f"{V1}/snmpConfig/192.168.1.1",
                  json=SNMP_CONFIG)
    client.get_snmp_config("192.168.1.1", location="Remote-DC")
    assert qs(responses.calls[0].request.url)["location"] == ["Remote-DC"]


@responses.activate
def test_set_snmp_config_v2c(client):
    responses.add(responses.PUT, f"{V1}/snmpConfig/192.168.1.1", status=204)
    new_config = {"version": "v2c", "community": "private", "port": 161}
    result = client.set_snmp_config("192.168.1.1", new_config)
    assert result is None
    body = json.loads(responses.calls[0].request.body)
    assert body["version"] == "v2c"
    assert body["community"] == "private"
    assert responses.calls[0].request.headers["Content-Type"] == "application/json"


@responses.activate
def test_set_snmp_config_v3(client):
    responses.add(responses.PUT, f"{V1}/snmpConfig/10.0.0.1", status=204)
    v3_config = {
        "version": "v3",
        "securityName": "myUser",
        "authPassphrase": "authSecret",
        "authProtocol": "SHA",
        "privPassphrase": "privSecret",
        "privProtocol": "AES128",
        "securityLevel": 3,
    }
    client.set_snmp_config("10.0.0.1", v3_config)
    body = json.loads(responses.calls[0].request.body)
    assert body["version"] == "v3"
    assert body["authProtocol"] == "SHA"
    assert body["securityLevel"] == 3
