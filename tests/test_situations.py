"""Tests for SituationsMixin – /api/v2/situations."""
import json
import responses
from .conftest import V2, qs
from .fixtures import SITUATION, SITUATION_LIST


@responses.activate
def test_get_situations_defaults(client):
    responses.add(responses.GET, f"{V2}/situations",
                  json=SITUATION_LIST)
    result = client.get_situations()
    assert result["alarm"][0]["isSituation"] is True
    assert result["alarm"][0]["id"] == 99
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["10"]
    assert params["offset"] == ["0"]


@responses.activate
def test_get_situations_pagination(client):
    responses.add(responses.GET, f"{V2}/situations",
                  json=SITUATION_LIST)
    client.get_situations(limit=25, offset=50)
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["25"]
    assert params["offset"] == ["50"]


@responses.activate
def test_create_situation(client):
    responses.add(responses.POST, f"{V2}/situations/create",
                  json=SITUATION, status=201)
    result = client.create_situation(
        alarm_ids=[42, 43],
        description="Correlated node-down event",
        diagnostic_text="Both devices share the same uplink.",
    )
    assert result["isSituation"] is True
    req = responses.calls[0].request
    body = json.loads(req.body)
    assert body["alarmIdList"] == "42,43"
    assert body["description"] == "Correlated node-down event"
    assert body["diagnosticText"] == "Both devices share the same uplink."
    assert req.headers["Content-Type"] == "application/json"


@responses.activate
def test_create_situation_minimal(client):
    responses.add(responses.POST, f"{V2}/situations/create",
                  json=SITUATION, status=201)
    client.create_situation(alarm_ids=[42])
    body = json.loads(responses.calls[0].request.body)
    assert body["alarmIdList"] == "42"
    assert "description" not in body
    assert "diagnosticText" not in body


@responses.activate
def test_add_alarms_to_situation(client):
    responses.add(responses.POST, f"{V2}/situations/associateAlarm",
                  json=SITUATION)
    result = client.add_alarms_to_situation(
        situation_id=99,
        alarm_ids=[44, 45],
        feedback="Confirmed related",
    )
    assert result["id"] == 99
    body = json.loads(responses.calls[0].request.body)
    assert body["situationId"] == 99
    assert body["alarmIdList"] == "44,45"
    assert body["feedback"] == "Confirmed related"


@responses.activate
def test_add_alarms_to_situation_no_feedback(client):
    responses.add(responses.POST, f"{V2}/situations/associateAlarm",
                  json=SITUATION)
    client.add_alarms_to_situation(situation_id=99, alarm_ids=[44])
    body = json.loads(responses.calls[0].request.body)
    assert "feedback" not in body


@responses.activate
def test_clear_situation(client):
    responses.add(responses.POST, f"{V2}/situations/clear",
                  status=204)
    result = client.clear_situation(99)
    assert result is None
    body = json.loads(responses.calls[0].request.body)
    assert body["situationId"] == 99


@responses.activate
def test_clear_situation_alarms(client):
    responses.add(responses.POST, f"{V2}/situations/alarms/clear",
                  status=204)
    result = client.clear_situation_alarms(99, alarm_ids=[42, 43])
    assert result is None
    body = json.loads(responses.calls[0].request.body)
    assert body["situationId"] == 99
    assert body["alarmIdList"] == "42,43"


@responses.activate
def test_accept_situation(client):
    responses.add(responses.POST, f"{V2}/situations/accepted/99",
                  status=204)
    result = client.accept_situation(99)
    assert result is None
    assert "/situations/accepted/99" in responses.calls[0].request.url


@responses.activate
def test_remove_alarms_from_situation(client):
    responses.add(responses.DELETE, f"{V2}/situations/removeAlarm",
                  status=204)
    result = client.remove_alarms_from_situation(99, alarm_ids=[42, 43])
    assert result is None
    assert responses.calls[0].request.method == "DELETE"
    params = qs(responses.calls[0].request.url)
    assert params["situationId"] == ["99"]
    assert params["alarmIdList"] == ["42,43"]
