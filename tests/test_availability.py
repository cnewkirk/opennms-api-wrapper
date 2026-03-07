"""Tests for AvailabilityMixin – /rest/availability."""
import responses
from .conftest import V1
from .fixtures import AVAILABILITY, AVAILABILITY_CATEGORY, AVAILABILITY_NODE


@responses.activate
def test_get_availability(client):
    responses.add(responses.GET, f"{V1}/availability", json=AVAILABILITY)
    result = client.get_availability()
    assert result["section"][0]["name"] == "Production"


@responses.activate
def test_get_availability_category(client):
    responses.add(responses.GET, f"{V1}/availability/categories/Production",
                  json=AVAILABILITY_CATEGORY)
    result = client.get_availability_category("Production")
    assert result["name"] == "Production"


@responses.activate
def test_get_availability_category_nodes(client):
    responses.add(responses.GET,
                  f"{V1}/availability/categories/Production/nodes",
                  json={"node": [AVAILABILITY_NODE]})
    result = client.get_availability_category_nodes("Production")
    assert result["node"][0]["id"] == 1


@responses.activate
def test_get_availability_category_node(client):
    responses.add(responses.GET,
                  f"{V1}/availability/categories/Production/nodes/1",
                  json=AVAILABILITY_NODE)
    result = client.get_availability_category_node("Production", 1)
    assert result["id"] == 1


@responses.activate
def test_get_availability_node(client):
    responses.add(responses.GET, f"{V1}/availability/nodes/1",
                  json=AVAILABILITY_NODE)
    result = client.get_availability_node(1)
    assert result["id"] == 1
    assert result["availability"] == 99.8
