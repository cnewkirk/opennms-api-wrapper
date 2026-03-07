"""Tests for IfServicesMixin – /rest/ifservices + v2."""
import responses
from .conftest import V1, V2, qs
from .fixtures import IF_SERVICE_LIST, IF_SERVICE_LIST_V2


@responses.activate
def test_get_ifservices(client):
    responses.add(responses.GET, f"{V1}/ifservices", json=IF_SERVICE_LIST)
    result = client.get_ifservices()
    assert result["service"][0]["id"] == 201


@responses.activate
def test_update_ifservices(client):
    responses.add(responses.PUT, f"{V1}/ifservices", status=204)
    result = client.update_ifservices(status="A")
    assert result is None
    assert "status=A" in responses.calls[0].request.body


@responses.activate
def test_get_ifservices_v2(client):
    responses.add(responses.GET, f"{V2}/ifservices", json=IF_SERVICE_LIST_V2)
    result = client.get_ifservices_v2(fiql="node.id==1")
    assert result["service"][0]["id"] == 201
    params = qs(responses.calls[0].request.url)
    assert params["_s"] == ["node.id==1"]
