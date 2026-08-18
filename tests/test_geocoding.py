"""Tests for GeocodingMixin – /api/v2/geocoding."""
import json

import responses
from .conftest import V2
from .fixtures import GEOCODING_CONFIG, GEOCODER_LIST


@responses.activate
def test_get_geocoding_config(client):
    responses.add(responses.GET, f"{V2}/geocoding/config",
                  json=GEOCODING_CONFIG)
    result = client.get_geocoding_config()
    assert result["activeGeocoderId"] == "nominatim"


@responses.activate
def test_get_geocoders(client):
    responses.add(responses.GET, f"{V2}/geocoding/geocoders",
                  json=GEOCODER_LIST)
    result = client.get_geocoders()
    assert result[0]["id"] == "nominatim"


@responses.activate
def test_get_geocoders_empty(client):
    responses.add(responses.GET, f"{V2}/geocoding/geocoders",
                  status=204)
    assert client.get_geocoders() is None


@responses.activate
def test_set_active_geocoder(client):
    responses.add(responses.POST, f"{V2}/geocoding/config",
                  status=202)
    client.set_active_geocoder("google")
    body = json.loads(responses.calls[0].request.body)
    assert body == {"activeGeocoderId": "google"}


@responses.activate
def test_configure_geocoder(client):
    responses.add(responses.POST, f"{V2}/geocoding/geocoders/google",
                  status=204)
    client.configure_geocoder("google", {"apiKey": "AIza..."})
    body = json.loads(responses.calls[0].request.body)
    assert body == {"config": {"apiKey": "AIza..."}}


@responses.activate
def test_reset_geocoding_config(client):
    responses.add(responses.DELETE, f"{V2}/geocoding/config",
                  status=202)
    assert client.reset_geocoding_config() is None
