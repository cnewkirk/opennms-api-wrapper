"""Tests for GraphMlMixin – /rest/graphml."""
import responses
from .conftest import V1
from .fixtures import GRAPHML_XML


@responses.activate
def test_get_graphml(client):
    responses.add(responses.GET, f"{V1}/graphml/my-graph",
                  body=GRAPHML_XML, content_type="application/xml")
    result = client.get_graphml("my-graph")
    assert "<graphml" in result


@responses.activate
def test_create_graphml(client):
    responses.add(responses.POST, f"{V1}/graphml/my-graph",
                  status=201)
    client.create_graphml("my-graph", GRAPHML_XML)
    request = responses.calls[0].request
    assert request.headers["Content-Type"] == "application/xml"
    assert request.body == GRAPHML_XML


@responses.activate
def test_delete_graphml(client):
    responses.add(responses.DELETE, f"{V1}/graphml/my-graph",
                  status=200)
    assert client.delete_graphml("my-graph") is None
