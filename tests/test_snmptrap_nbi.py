"""Tests for SnmpTrapNbiMixin – /rest/config/snmptrap-nbi."""
import json
import responses
from .conftest import V1
from .fixtures import (
    SNMPTRAP_NBI_CONFIG, SNMPTRAP_NBI_STATUS,
    SNMPTRAP_NBI_TRAPSINK, SNMPTRAP_NBI_TRAPSINK_LIST,
)


@responses.activate
def test_get_snmptrap_nbi_config(client):
    responses.add(responses.GET, f"{V1}/config/snmptrap-nbi",
                  json=SNMPTRAP_NBI_CONFIG)
    result = client.get_snmptrap_nbi_config()
    assert result["enabled"] is True


@responses.activate
def test_get_snmptrap_nbi_status(client):
    responses.add(responses.GET, f"{V1}/config/snmptrap-nbi/status",
                  json=SNMPTRAP_NBI_STATUS)
    result = client.get_snmptrap_nbi_status()
    assert result["enabled"] is True


@responses.activate
def test_set_snmptrap_nbi_status(client):
    responses.add(responses.PUT, f"{V1}/config/snmptrap-nbi/status",
                  status=204)
    result = client.set_snmptrap_nbi_status(False)
    assert result is None
    assert "enabled=false" in responses.calls[0].request.body


@responses.activate
def test_get_snmptrap_nbi_trapsinks(client):
    responses.add(responses.GET,
                  f"{V1}/config/snmptrap-nbi/trapsinks",
                  json=SNMPTRAP_NBI_TRAPSINK_LIST)
    result = client.get_snmptrap_nbi_trapsinks()
    assert result["trapsink"][0]["name"] == "remote-nms"


@responses.activate
def test_get_snmptrap_nbi_trapsink(client):
    responses.add(responses.GET,
                  f"{V1}/config/snmptrap-nbi/trapsinks/remote-nms",
                  json=SNMPTRAP_NBI_TRAPSINK)
    result = client.get_snmptrap_nbi_trapsink("remote-nms")
    assert result["ipAddress"] == "10.0.0.1"


@responses.activate
def test_create_snmptrap_nbi_trapsink(client):
    responses.add(responses.POST,
                  f"{V1}/config/snmptrap-nbi/trapsinks",
                  status=201)
    data = {"name": "new-sink", "ipAddress": "10.0.0.2",
            "port": 162, "community": "public"}
    client.create_snmptrap_nbi_trapsink(data)
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "new-sink"


@responses.activate
def test_update_snmptrap_nbi_trapsink(client):
    responses.add(responses.PUT,
                  f"{V1}/config/snmptrap-nbi/trapsinks/remote-nms",
                  status=204)
    result = client.update_snmptrap_nbi_trapsink("remote-nms",
                                                  {"port": "163"})
    assert result is None
    assert "port=163" in responses.calls[0].request.body


@responses.activate
def test_delete_snmptrap_nbi_trapsink(client):
    responses.add(responses.DELETE,
                  f"{V1}/config/snmptrap-nbi/trapsinks/remote-nms",
                  status=204)
    result = client.delete_snmptrap_nbi_trapsink("remote-nms")
    assert result is None


@responses.activate
def test_update_snmptrap_nbi_config(client):
    responses.add(responses.POST, f"{V1}/config/snmptrap-nbi",
                  status=204)
    result = client.update_snmptrap_nbi_config({"enabled": False})
    assert result is None
