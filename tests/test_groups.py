"""Tests for GroupsMixin – /rest/groups."""
import json
import responses
from .conftest import V1
from .fixtures import GROUP, GROUP_LIST, GROUP_USER_LIST, GROUP_CATEGORY_LIST


@responses.activate
def test_get_groups(client):
    responses.add(responses.GET, f"{V1}/groups", json=GROUP_LIST)
    result = client.get_groups()
    assert result["group"][0]["name"] == "network-ops"


@responses.activate
def test_get_group(client):
    responses.add(responses.GET, f"{V1}/groups/network-ops", json=GROUP)
    result = client.get_group("network-ops")
    assert result["name"] == "network-ops"
    assert result["comments"] == "Network operations team"


@responses.activate
def test_create_group(client):
    responses.add(responses.POST, f"{V1}/groups", json=GROUP, status=201)
    client.create_group({"name": "network-ops", "comments": "Network operations team"})
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "network-ops"
    assert responses.calls[0].request.headers["Content-Type"] == "application/json"


@responses.activate
def test_update_group(client):
    responses.add(responses.PUT, f"{V1}/groups/network-ops", status=204)
    client.update_group("network-ops", {"comments": "Updated comment"})
    body = json.loads(responses.calls[0].request.body)
    assert body["comments"] == "Updated comment"


@responses.activate
def test_delete_group(client):
    responses.add(responses.DELETE, f"{V1}/groups/network-ops", status=202)
    result = client.delete_group("network-ops")
    assert result is None


@responses.activate
def test_get_group_users(client):
    responses.add(responses.GET, f"{V1}/groups/network-ops/users",
                  json=GROUP_USER_LIST)
    result = client.get_group_users("network-ops")
    assert "admin" in result["users"]


@responses.activate
def test_add_user_to_group(client):
    responses.add(responses.PUT, f"{V1}/groups/network-ops/users/jsmith",
                  status=204)
    result = client.add_user_to_group("network-ops", "jsmith")
    assert result is None
    assert "/groups/network-ops/users/jsmith" in responses.calls[0].request.url


@responses.activate
def test_remove_user_from_group(client):
    responses.add(responses.DELETE, f"{V1}/groups/network-ops/users/jsmith",
                  status=204)
    result = client.remove_user_from_group("network-ops", "jsmith")
    assert result is None


@responses.activate
def test_get_group_categories(client):
    responses.add(responses.GET, f"{V1}/groups/network-ops/categories",
                  json=GROUP_CATEGORY_LIST)
    result = client.get_group_categories("network-ops")
    assert "Production" in result["categories"]


@responses.activate
def test_add_category_to_group(client):
    responses.add(responses.PUT,
                  f"{V1}/groups/network-ops/categories/Production",
                  status=204)
    result = client.add_category_to_group("network-ops", "Production")
    assert result is None


@responses.activate
def test_remove_category_from_group(client):
    responses.add(responses.DELETE,
                  f"{V1}/groups/network-ops/categories/Production",
                  status=204)
    result = client.remove_category_from_group("network-ops", "Production")
    assert result is None
