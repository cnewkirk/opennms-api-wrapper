"""Tests for EmailNbiMixin – /rest/config/email-nbi."""
import json
import responses
from .conftest import V1
from .fixtures import (
    EMAIL_NBI_CONFIG, EMAIL_NBI_STATUS,
    EMAIL_NBI_DESTINATION, EMAIL_NBI_DESTINATION_LIST,
)


@responses.activate
def test_get_email_nbi_config(client):
    responses.add(responses.GET, f"{V1}/config/email-nbi",
                  json=EMAIL_NBI_CONFIG)
    result = client.get_email_nbi_config()
    assert result["enabled"] is False


@responses.activate
def test_get_email_nbi_status(client):
    responses.add(responses.GET, f"{V1}/config/email-nbi/status",
                  json=EMAIL_NBI_STATUS)
    result = client.get_email_nbi_status()
    assert result["enabled"] is False


@responses.activate
def test_set_email_nbi_status(client):
    responses.add(responses.PUT, f"{V1}/config/email-nbi/status",
                  status=204)
    result = client.set_email_nbi_status(True)
    assert result is None
    assert "enabled=true" in responses.calls[0].request.body


@responses.activate
def test_get_email_nbi_destinations(client):
    responses.add(responses.GET, f"{V1}/config/email-nbi/destinations",
                  json=EMAIL_NBI_DESTINATION_LIST)
    result = client.get_email_nbi_destinations()
    assert result["destination"][0]["name"] == "ops-team"


@responses.activate
def test_get_email_nbi_destination(client):
    responses.add(responses.GET,
                  f"{V1}/config/email-nbi/destinations/ops-team",
                  json=EMAIL_NBI_DESTINATION)
    result = client.get_email_nbi_destination("ops-team")
    assert result["name"] == "ops-team"


@responses.activate
def test_create_email_nbi_destination(client):
    responses.add(responses.POST,
                  f"{V1}/config/email-nbi/destinations", status=201)
    data = {"name": "new-dest", "firstOccurrenceOnly": True}
    client.create_email_nbi_destination(data)
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "new-dest"


@responses.activate
def test_update_email_nbi_destination(client):
    responses.add(responses.PUT,
                  f"{V1}/config/email-nbi/destinations/ops-team",
                  status=204)
    result = client.update_email_nbi_destination("ops-team",
                                                  {"firstOccurrenceOnly": "false"})
    assert result is None


@responses.activate
def test_delete_email_nbi_destination(client):
    responses.add(responses.DELETE,
                  f"{V1}/config/email-nbi/destinations/ops-team",
                  status=204)
    result = client.delete_email_nbi_destination("ops-team")
    assert result is None


@responses.activate
def test_update_email_nbi_config(client):
    responses.add(responses.POST, f"{V1}/config/email-nbi", status=204)
    result = client.update_email_nbi_config({"enabled": True})
    assert result is None
