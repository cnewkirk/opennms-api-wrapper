"""Tests for AcksMixin – /rest/acks."""
import responses
from urllib.parse import parse_qs
from .conftest import V1, qs
from .fixtures import ACKNOWLEDGEMENT, ACKNOWLEDGEMENT_LIST


@responses.activate
def test_get_acks_default(client):
    responses.add(responses.GET, f"{V1}/acks", json=ACKNOWLEDGEMENT_LIST)
    result = client.get_acks()
    assert result["ack"][0]["id"] == 701
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["10"]
    assert params["offset"] == ["0"]


@responses.activate
def test_get_acks_with_filters(client):
    responses.add(responses.GET, f"{V1}/acks", json=ACKNOWLEDGEMENT_LIST)
    client.get_acks(limit=25, ackUser="admin")
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["25"]
    assert params["ackUser"] == ["admin"]


@responses.activate
def test_get_ack(client):
    responses.add(responses.GET, f"{V1}/acks/701", json=ACKNOWLEDGEMENT)
    result = client.get_ack(701)
    assert result["id"] == 701
    assert result["ackAction"] == "ACKNOWLEDGE"


@responses.activate
def test_get_ack_count(client):
    responses.add(responses.GET, f"{V1}/acks/count",
                  body="23", content_type="text/plain")
    assert client.get_ack_count() == 23


@responses.activate
def test_create_ack_alarm(client):
    responses.add(responses.POST, f"{V1}/acks", json=ACKNOWLEDGEMENT, status=200)
    client.create_ack("ack", alarm_id=42)
    req = responses.calls[0].request
    # acks POST uses form-encoded data per API docs
    body = parse_qs(req.body)
    assert body["action"] == ["ack"]
    assert body["alarmId"] == ["42"]


@responses.activate
def test_create_ack_notification(client):
    responses.add(responses.POST, f"{V1}/acks", json=ACKNOWLEDGEMENT, status=200)
    client.create_ack("ack", notification_id=601)
    body = parse_qs(responses.calls[0].request.body)
    assert body["action"] == ["ack"]
    assert body["notifId"] == ["601"]


@responses.activate
def test_create_ack_escalate(client):
    responses.add(responses.POST, f"{V1}/acks", json=ACKNOWLEDGEMENT, status=200)
    client.create_ack("esc", alarm_id=42)
    body = parse_qs(responses.calls[0].request.body)
    assert body["action"] == ["esc"]
    assert body["alarmId"] == ["42"]


@responses.activate
def test_ack_notification(client):
    responses.add(responses.POST, f"{V1}/acks", json=ACKNOWLEDGEMENT, status=200)
    client.ack_notification(601)
    body = parse_qs(responses.calls[0].request.body)
    assert body["action"] == ["ack"]
    assert body["notifId"] == ["601"]


@responses.activate
def test_unack_notification(client):
    responses.add(responses.POST, f"{V1}/acks", json=ACKNOWLEDGEMENT, status=200)
    client.unack_notification(601)
    body = parse_qs(responses.calls[0].request.body)
    assert body["action"] == ["unack"]
    assert body["notifId"] == ["601"]
