"""Tests for EventsMixin – /rest/events."""
import json
import responses
from .conftest import FORM, V1, add_contract, qs
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
    add_contract(responses.PUT, f"{V1}/events/1001", FORM)
    result = client.ack_event(1001)
    assert result is None
    assert responses.calls[0].request.body == "ack=true"


@responses.activate
def test_unack_event(client):
    add_contract(responses.PUT, f"{V1}/events/1001", FORM)
    client.unack_event(1001)
    assert responses.calls[0].request.body == "ack=false"


@responses.activate
def test_bulk_ack_events(client):
    add_contract(responses.PUT, f"{V1}/events", FORM)
    client.bulk_ack_events(nodeId=1)
    body = responses.calls[0].request.body
    assert "ack=true" in body
    assert "nodeId=1" in body


@responses.activate
def test_bulk_unack_events(client):
    add_contract(responses.PUT, f"{V1}/events", FORM)
    client.bulk_unack_events()
    assert responses.calls[0].request.body == "ack=false"
