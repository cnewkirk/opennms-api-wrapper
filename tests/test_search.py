"""Tests for SearchMixin – /api/v2/search."""
import responses
from .conftest import V2, qs
from .fixtures import SEARCH_RESULTS


@responses.activate
def test_search(client):
    responses.add(responses.GET, f"{V2}/search", json=SEARCH_RESULTS)
    result = client.search("router")
    assert result[0]["context"] == "Node"
    assert qs(responses.calls[0].request.url)["_s"] == ["router"]


@responses.activate
def test_search_with_context_and_limit(client):
    responses.add(responses.GET, f"{V2}/search", json=SEARCH_RESULTS)
    client.search("router", context="Node", limit=5)
    params = qs(responses.calls[0].request.url)
    assert params["_c"] == ["Node"]
    assert params["_l"] == ["5"]


@responses.activate
def test_search_no_matches(client):
    responses.add(responses.GET, f"{V2}/search", status=204)
    assert client.search("nothing-matches-this") is None
