"""Tests for MapsMixin – /rest/maps."""
import json
import responses
from .conftest import V1
from .fixtures import MAP, MAP_LIST, MAP_ELEMENTS


@responses.activate
def test_get_maps(client):
    responses.add(responses.GET, f"{V1}/maps", json=MAP_LIST)
    result = client.get_maps()
    assert result["map"][0]["id"] == 1
    assert result["map"][0]["name"] == "Core Network"


@responses.activate
def test_get_map(client):
    responses.add(responses.GET, f"{V1}/maps/1", json=MAP)
    result = client.get_map(1)
    assert result["id"] == 1
    assert result["accessMode"] == "RW"


@responses.activate
def test_get_map_elements(client):
    responses.add(responses.GET, f"{V1}/maps/1/mapElements", json=MAP_ELEMENTS)
    result = client.get_map_elements(1)
    assert result["mapElement"][0]["elementId"] == 1
    assert result["mapElement"][0]["type"] == "N"
    assert "/maps/1/mapElements" in responses.calls[0].request.url


@responses.activate
def test_create_map(client):
    responses.add(responses.POST, f"{V1}/maps", json=MAP, status=201)
    new_map = {"name": "Core Network", "mapWidth": 1024, "mapHeight": 768,
               "accessMode": "RW", "owner": "admin"}
    result = client.create_map(new_map)
    assert result["id"] == 1
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "Core Network"


@responses.activate
def test_update_map(client):
    responses.add(responses.PUT, f"{V1}/maps/1", status=204)
    client.update_map(1, {"name": "Updated Map Name"})
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "Updated Map Name"


@responses.activate
def test_delete_map(client):
    responses.add(responses.DELETE, f"{V1}/maps/1", status=204)
    result = client.delete_map(1)
    assert result is None
