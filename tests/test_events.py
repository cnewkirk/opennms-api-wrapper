"""Tests for EventsMixin – /rest/events."""
import json
import responses
from .conftest import V1, qs
from .fixtures import EVENT, EVENT_LIST

NEW_EVENT = {
    "uei": "uei.opennms.org/internal/test",
    "source": "pytest",
    "severity": "Normal",
}


@responses.activate
def test_get_events_default(client):
    responses.add(responses.GET, f"{V1}/events", json=EVENT_LIST)
    result = client.get_events()
    assert result["event"][0]["id"] == 1001
    assert result["totalCount"] == 1
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["10"]
    assert params["offset"] == ["0"]


@responses.activate
def test_get_events_with_filters(client):
    responses.add(responses.GET, f"{V1}/events", json=EVENT_LIST)
    client.get_events(limit=50, uei="uei.opennms.org/nodes/nodeDown",
                      order_by="eventTime", order="descending")
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["50"]
    assert params["uei"] == ["uei.opennms.org/nodes/nodeDown"]
    assert params["orderBy"] == ["eventTime"]
    assert params["order"] == ["descending"]


@responses.activate
def test_get_event(client):
    responses.add(responses.GET, f"{V1}/events/1001", json=EVENT)
    result = client.get_event(1001)
    assert result["id"] == 1001
    assert result["severity"] == "MAJOR"


@responses.activate
def test_get_event_count(client):
    responses.add(responses.GET, f"{V1}/events/count",
                  body="1337", content_type="text/plain")
    result = client.get_event_count()
    assert result == 1337


@responses.activate
def test_create_event(client):
    responses.add(responses.POST, f"{V1}/events", status=200)
    client.create_event(NEW_EVENT)
    req = responses.calls[0].request
    body = json.loads(req.body)
    assert body["uei"] == "uei.opennms.org/internal/test"
    assert body["source"] == "pytest"
    assert req.headers["Content-Type"] == "application/json"


@responses.activate
def test_ack_event(client):
    responses.add(responses.PUT, f"{V1}/events/1001", status=204)
    result = client.ack_event(1001)
    assert result is None
    assert qs(responses.calls[0].request.url)["ack"] == ["true"]


@responses.activate
def test_unack_event(client):
    responses.add(responses.PUT, f"{V1}/events/1001", status=204)
    client.unack_event(1001)
    assert qs(responses.calls[0].request.url)["ack"] == ["false"]


@responses.activate
def test_bulk_ack_events(client):
    responses.add(responses.PUT, f"{V1}/events", status=204)
    client.bulk_ack_events(nodeId=1)
    params = qs(responses.calls[0].request.url)
    assert params["ack"] == ["true"]
    assert params["nodeId"] == ["1"]


@responses.activate
def test_bulk_unack_events(client):
    responses.add(responses.PUT, f"{V1}/events", status=204)
    client.bulk_unack_events()
    assert qs(responses.calls[0].request.url)["ack"] == ["false"]
