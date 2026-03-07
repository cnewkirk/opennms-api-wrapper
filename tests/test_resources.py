"""Tests for ResourcesMixin – /rest/resources."""
import responses
from .conftest import V1, qs
from .fixtures import RESOURCE, RESOURCE_TREE


@responses.activate
def test_get_resources(client):
    responses.add(responses.GET, f"{V1}/resources", json=RESOURCE_TREE)
    result = client.get_resources()
    assert result["resource"]["id"].startswith("node[1]")
    assert qs(responses.calls[0].request.url)["depth"] == ["1"]


@responses.activate
def test_get_resources_custom_depth(client):
    responses.add(responses.GET, f"{V1}/resources", json=RESOURCE_TREE)
    client.get_resources(depth=-1)
    assert qs(responses.calls[0].request.url)["depth"] == ["-1"]


@responses.activate
def test_get_resource(client):
    rid = "node[1].interfaceSnmp[eth0-04013f75f101]"
    responses.add(responses.GET, f"{V1}/resources/{rid}", json=RESOURCE_TREE)
    result = client.get_resource(rid)
    assert result["resource"]["id"] == rid
    assert qs(responses.calls[0].request.url)["depth"] == ["-1"]


@responses.activate
def test_get_resources_for_node(client):
    responses.add(responses.GET, f"{V1}/resources/fornode/1", json=RESOURCE_TREE)
    result = client.get_resources_for_node("1")
    assert result["resource"]["parentId"] == "node[1]"


@responses.activate
def test_get_resources_select(client):
    responses.add(responses.GET, f"{V1}/resources/select", json=RESOURCE_TREE)
    client.get_resources_select(
        nodes=[1, 2],
        node_subresources=["interfaceSnmp"],
        string_properties=["ifAlias"],
    )
    params = qs(responses.calls[0].request.url)
    assert params["nodes"] == ["1,2"]
    assert params["nodeSubresources"] == ["interfaceSnmp"]
    assert params["stringProperties"] == ["ifAlias"]


@responses.activate
def test_delete_resource(client):
    rid = "node[1].interfaceSnmp[eth0-04013f75f101]"
    responses.add(responses.DELETE, f"{V1}/resources/{rid}", status=204)
    result = client.delete_resource(rid)
    assert result is None
    assert responses.calls[0].request.method == "DELETE"
