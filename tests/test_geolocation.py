"""Tests for GeolocationMixin – /api/v2/geolocation."""
import json

import responses
from .conftest import V2
from .fixtures import GEOLOCATION_CONFIG, GEOLOCATION_LIST


@responses.activate
def test_get_geolocation_config(client):
    responses.add(responses.GET, f"{V2}/geolocation/config",
                  json=GEOLOCATION_CONFIG)
    result = client.get_geolocation_config()
    assert result["tileServerName"] == "OpenStreetMap"


@responses.activate
def test_query_geolocations(client):
    responses.add(responses.POST, f"{V2}/geolocation",
                  json=GEOLOCATION_LIST)
    result = client.query_geolocations(
        strategy="Outages", severity_filter="Major",
        include_acknowledged_alarms=True)
    assert result[0]["nodeInfo"]["nodeLabel"] == "router-01"
    body = json.loads(responses.calls[0].request.body)
    assert body["strategy"] == "Outages"
    assert body["severityFilter"] == "Major"
    assert body["includeAcknowledgedAlarms"] is True


@responses.activate
def test_query_geolocations_defaults(client):
    responses.add(responses.POST, f"{V2}/geolocation", status=204)
    assert client.query_geolocations() is None
    body = json.loads(responses.calls[0].request.body)
    assert body == {"strategy": "Alarms"}
