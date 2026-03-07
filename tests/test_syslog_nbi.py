"""Tests for SyslogNbiMixin – /rest/config/syslog-nbi."""
import json
import responses
from .conftest import V1
from .fixtures import (
    SYSLOG_NBI_CONFIG, SYSLOG_NBI_STATUS,
    SYSLOG_NBI_DESTINATION, SYSLOG_NBI_DESTINATION_LIST,
)


@responses.activate
def test_get_syslog_nbi_config(client):
    responses.add(responses.GET, f"{V1}/config/syslog-nbi",
                  json=SYSLOG_NBI_CONFIG)
    result = client.get_syslog_nbi_config()
    assert result["enabled"] is False


@responses.activate
def test_get_syslog_nbi_status(client):
    responses.add(responses.GET, f"{V1}/config/syslog-nbi/status",
                  json=SYSLOG_NBI_STATUS)
    result = client.get_syslog_nbi_status()
    assert result["enabled"] is False


@responses.activate
def test_set_syslog_nbi_status(client):
    responses.add(responses.PUT, f"{V1}/config/syslog-nbi/status",
                  status=204)
    result = client.set_syslog_nbi_status(True)
    assert result is None
    assert "enabled=true" in responses.calls[0].request.body


@responses.activate
def test_get_syslog_nbi_destinations(client):
    responses.add(responses.GET,
                  f"{V1}/config/syslog-nbi/destinations",
                  json=SYSLOG_NBI_DESTINATION_LIST)
    result = client.get_syslog_nbi_destinations()
    assert result["destination"][0]["name"] == "siem"


@responses.activate
def test_get_syslog_nbi_destination(client):
    responses.add(responses.GET,
                  f"{V1}/config/syslog-nbi/destinations/siem",
                  json=SYSLOG_NBI_DESTINATION)
    result = client.get_syslog_nbi_destination("siem")
    assert result["host"] == "10.0.0.2"


@responses.activate
def test_create_syslog_nbi_destination(client):
    responses.add(responses.POST,
                  f"{V1}/config/syslog-nbi/destinations", status=201)
    data = {"name": "new-syslog", "host": "10.0.0.3", "port": 514}
    client.create_syslog_nbi_destination(data)
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "new-syslog"


@responses.activate
def test_update_syslog_nbi_destination(client):
    responses.add(responses.PUT,
                  f"{V1}/config/syslog-nbi/destinations/siem",
                  status=204)
    result = client.update_syslog_nbi_destination("siem",
                                                   {"port": "515"})
    assert result is None


@responses.activate
def test_delete_syslog_nbi_destination(client):
    responses.add(responses.DELETE,
                  f"{V1}/config/syslog-nbi/destinations/siem",
                  status=204)
    result = client.delete_syslog_nbi_destination("siem")
    assert result is None


@responses.activate
def test_update_syslog_nbi_config(client):
    responses.add(responses.POST, f"{V1}/config/syslog-nbi", status=204)
    result = client.update_syslog_nbi_config({"enabled": True})
    assert result is None
