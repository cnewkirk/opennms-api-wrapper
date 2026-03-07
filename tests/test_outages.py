"""Tests for OutagesMixin – /rest/outages."""
import responses
from .conftest import V1, qs
from .fixtures import OUTAGE, OUTAGE_LIST


@responses.activate
def test_get_outages_default(client):
    responses.add(responses.GET, f"{V1}/outages", json=OUTAGE_LIST)
    result = client.get_outages()
    assert result["outage"][0]["id"] == 501
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["10"]
    assert params["offset"] == ["0"]


@responses.activate
def test_get_outages_with_filters(client):
    responses.add(responses.GET, f"{V1}/outages", json=OUTAGE_LIST)
    client.get_outages(limit=25, order_by="ifLostService",
                       order="descending", ifRegainedService="null")
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["25"]
    assert params["orderBy"] == ["ifLostService"]
    assert params["order"] == ["descending"]
    assert params["ifRegainedService"] == ["null"]


@responses.activate
def test_get_outage(client):
    responses.add(responses.GET, f"{V1}/outages/501", json=OUTAGE)
    result = client.get_outage(501)
    assert result["id"] == 501
    assert result["ifRegainedService"] is None


@responses.activate
def test_get_outage_count(client):
    responses.add(responses.GET, f"{V1}/outages/count",
                  body="17", content_type="text/plain")
    assert client.get_outage_count() == 17


@responses.activate
def test_get_node_outages(client):
    responses.add(responses.GET, f"{V1}/outages/forNode/1", json=OUTAGE_LIST)
    result = client.get_node_outages(1)
    assert result["outage"][0]["node"]["id"] == 1
    assert responses.calls[0].request.url.endswith("/outages/forNode/1")
