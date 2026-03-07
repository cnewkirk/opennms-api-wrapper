"""Tests for GraphsMixin prefab graph methods – /rest/graphs."""
import responses
from .conftest import V1
from .fixtures import (
    PREFAB_GRAPH_NAMES, PREFAB_GRAPH,
    PREFAB_GRAPHS_FOR_RESOURCE, PREFAB_GRAPHS_FOR_NODE,
)


@responses.activate
def test_get_prefab_graph_names(client):
    responses.add(responses.GET, f"{V1}/graphs", json=PREFAB_GRAPH_NAMES)
    result = client.get_prefab_graph_names()
    assert "mib2.bits" in result


@responses.activate
def test_get_prefab_graph(client):
    responses.add(responses.GET, f"{V1}/graphs/mib2.bits",
                  json=PREFAB_GRAPH)
    result = client.get_prefab_graph("mib2.bits")
    assert result["name"] == "mib2.bits"


@responses.activate
def test_get_prefab_graphs_for_resource(client):
    rid = "node[1].interfaceSnmp[eth0-04013f75f101]"
    responses.add(responses.GET,
                  f"{V1}/graphs/for/{rid}",
                  json=PREFAB_GRAPHS_FOR_RESOURCE)
    result = client.get_prefab_graphs_for_resource(rid)
    assert "mib2.bits" in result["name"]


@responses.activate
def test_get_prefab_graphs_for_node(client):
    responses.add(responses.GET, f"{V1}/graphs/fornode/1",
                  json=PREFAB_GRAPHS_FOR_NODE)
    result = client.get_prefab_graphs_for_node("1")
    assert "mib2.bits" in result["name"]
