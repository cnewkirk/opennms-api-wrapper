"""Tests for MonitoringLocationsMixin – /rest/monitoringLocations."""
import json
import responses
from .conftest import V1, qs
from .fixtures import MONITORING_LOCATION, MONITORING_LOCATION_LIST


@responses.activate
def test_get_monitoring_locations(client):
    responses.add(responses.GET, f"{V1}/monitoringLocations",
                  json=MONITORING_LOCATION_LIST)
    result = client.get_monitoring_locations()
    assert result["location"][0]["location-name"] == "Default"


@responses.activate
def test_get_monitoring_location(client):
    responses.add(responses.GET, f"{V1}/monitoringLocations/Default",
                  json=MONITORING_LOCATION)
    result = client.get_monitoring_location("Default")
    assert result["location-name"] == "Default"


@responses.activate
def test_get_default_monitoring_location(client):
    responses.add(responses.GET, f"{V1}/monitoringLocations/default",
                  json=MONITORING_LOCATION)
    result = client.get_default_monitoring_location()
    assert result["location-name"] == "Default"


@responses.activate
def test_get_monitoring_location_count(client):
    responses.add(responses.GET, f"{V1}/monitoringLocations/count",
                  body="3", content_type="text/plain")
    assert client.get_monitoring_location_count() == 3


@responses.activate
def test_create_monitoring_location(client):
    responses.add(responses.POST, f"{V1}/monitoringLocations",
                  status=201)
    payload = {"location-name": "Remote", "monitoring-area": "remote"}
    result = client.create_monitoring_location(payload)
    body = json.loads(responses.calls[0].request.body)
    assert body["location-name"] == "Remote"


@responses.activate
def test_update_monitoring_location(client):
    responses.add(responses.PUT, f"{V1}/monitoringLocations/Default",
                  status=204)
    result = client.update_monitoring_location("Default",
                                               {"monitoring-area": "updated"})
    assert result is None
    assert "monitoring-area=updated" in responses.calls[0].request.body


@responses.activate
def test_delete_monitoring_location(client):
    responses.add(responses.DELETE, f"{V1}/monitoringLocations/Remote",
                  status=204)
    result = client.delete_monitoring_location("Remote")
    assert result is None
