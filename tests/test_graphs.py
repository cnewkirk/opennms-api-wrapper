"""Tests for GraphsMixin – /rest/graphs."""
import json
import responses
from .conftest import V1, qs
from .fixtures import GRAPH_CONTAINER, GRAPH_CONTAINER_LIST, GRAPH, \
    GRAPH_SUGGESTIONS, GRAPH_SEARCH_RESULTS


@responses.activate
def test_get_graph_containers(client):
    responses.add(responses.GET, f"{V1}/graphs", json=GRAPH_CONTAINER_LIST)
    result = client.get_graph_containers()
    assert result["graphContainer"][0]["id"] == "nodes"


@responses.activate
def test_get_graph_container(client):
    responses.add(responses.GET, f"{V1}/graphs/nodes", json=GRAPH_CONTAINER)
    result = client.get_graph_container("nodes")
    assert result["id"] == "nodes"
    assert result["label"] == "Nodes"


@responses.activate
def test_get_graph(client):
    responses.add(responses.GET, f"{V1}/graphs/nodes/nodes", json=GRAPH)
    result = client.get_graph("nodes", "nodes")
    assert result["namespace"] == "nodes"
    assert "/graphs/nodes/nodes" in responses.calls[0].request.url


@responses.activate
def test_get_graph_view_default(client):
    responses.add(responses.POST, f"{V1}/graphs/nodes/nodes", json=GRAPH)
    result = client.get_graph_view("nodes", "nodes")
    assert result["namespace"] == "nodes"
    req = responses.calls[0].request
    body = json.loads(req.body)
    assert body["semanticZoomLevel"] == 1
    assert body["verticesInFocus"] == []


@responses.activate
def test_get_graph_view_with_focus(client):
    responses.add(responses.POST, f"{V1}/graphs/nodes/nodes", json=GRAPH)
    client.get_graph_view("nodes", "nodes",
                          semantic_zoom_level=2,
                          vertices_in_focus=["nodes:1", "nodes:2"])
    body = json.loads(responses.calls[0].request.body)
    assert body["semanticZoomLevel"] == 2
    assert "nodes:1" in body["verticesInFocus"]


@responses.activate
def test_get_graph_search_suggestions(client):
    responses.add(responses.GET, f"{V1}/graphs/search/suggestions/nodes",
                  json=GRAPH_SUGGESTIONS)
    result = client.get_graph_search_suggestions("nodes", "router01")
    assert result["suggestion"][0]["label"] == "router01.example.com"
    assert qs(responses.calls[0].request.url)["s"] == ["router01"]


@responses.activate
def test_get_graph_search_results(client):
    responses.add(responses.GET, f"{V1}/graphs/search/results/nodes",
                  json=GRAPH_SEARCH_RESULTS)
    result = client.get_graph_search_results(
        "nodes", provider_id="NodeSearchProvider", criteria="router01")
    assert result["searchResult"][0]["namespace"] == "nodes"
    params = qs(responses.calls[0].request.url)
    assert params["providerId"] == ["NodeSearchProvider"]
    assert params["criteria"] == ["router01"]
