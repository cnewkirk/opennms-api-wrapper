"""Tests for CategoriesMixin – /rest/categories."""
import json
import responses
from .conftest import V1
from .fixtures import CATEGORY, CATEGORY_LIST


@responses.activate
def test_get_categories(client):
    responses.add(responses.GET, f"{V1}/categories", json=CATEGORY_LIST)
    result = client.get_categories()
    assert result["category"][0]["name"] == "Production"


@responses.activate
def test_get_category(client):
    responses.add(responses.GET, f"{V1}/categories/Production", json=CATEGORY)
    result = client.get_category("Production")
    assert result["id"] == 2
    assert result["name"] == "Production"


@responses.activate
def test_create_category(client):
    responses.add(responses.POST, f"{V1}/categories", json=CATEGORY, status=201)
    client.create_category({"name": "Production", "authorizedGroups": []})
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "Production"


@responses.activate
def test_update_category(client):
    responses.add(responses.PUT, f"{V1}/categories/Production", status=204)
    client.update_category("Production", {"name": "Production",
                                          "authorizedGroups": ["network-ops"]})
    body = json.loads(responses.calls[0].request.body)
    assert "network-ops" in body["authorizedGroups"]


@responses.activate
def test_delete_category(client):
    responses.add(responses.DELETE, f"{V1}/categories/Production", status=204)
    result = client.delete_category("Production")
    assert result is None


@responses.activate
def test_get_node_categories_list(client):
    responses.add(responses.GET, f"{V1}/categories/nodes/1",
                  json=CATEGORY_LIST)
    result = client.get_node_categories_list(1)
    assert result["category"][0]["name"] == "Production"
    assert "/categories/nodes/1" in responses.calls[0].request.url


@responses.activate
def test_get_category_for_node(client):
    responses.add(responses.GET, f"{V1}/categories/Production/nodes/1",
                  json=CATEGORY)
    result = client.get_category_for_node("Production", 1)
    assert result["name"] == "Production"


@responses.activate
def test_associate_category_with_node(client):
    responses.add(responses.PUT, f"{V1}/categories/Production/nodes/1",
                  status=204)
    result = client.associate_category_with_node("Production", 1)
    assert result is None


@responses.activate
def test_dissociate_category_from_node(client):
    responses.add(responses.DELETE, f"{V1}/categories/Production/nodes/1",
                  status=204)
    result = client.dissociate_category_from_node("Production", 1)
    assert result is None


@responses.activate
def test_get_categories_for_group(client):
    responses.add(responses.GET, f"{V1}/categories/groups/network-ops",
                  json=CATEGORY_LIST)
    result = client.get_categories_for_group("network-ops")
    assert "/categories/groups/network-ops" in responses.calls[0].request.url


@responses.activate
def test_associate_category_with_group(client):
    responses.add(responses.PUT,
                  f"{V1}/categories/Production/groups/network-ops",
                  status=204)
    result = client.associate_category_with_group("Production", "network-ops")
    assert result is None


@responses.activate
def test_dissociate_category_from_group(client):
    responses.add(responses.DELETE,
                  f"{V1}/categories/Production/groups/network-ops",
                  status=204)
    result = client.dissociate_category_from_group("Production", "network-ops")
    assert result is None
