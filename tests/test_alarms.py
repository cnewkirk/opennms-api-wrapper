"""Tests for AlarmsMixin – /rest/alarms and /api/v2/alarms."""
import responses
from .conftest import V1, V2, qs
from .fixtures import ALARM, ALARM_LIST


@responses.activate
def test_get_alarms_default(client):
    responses.add(responses.GET, f"{V1}/alarms", json=ALARM_LIST)
    result = client.get_alarms()
    assert result["alarm"][0]["id"] == 42
    assert result["totalCount"] == 1
    req = responses.calls[0].request
    assert qs(req.url)["limit"] == ["10"]
    assert qs(req.url)["offset"] == ["0"]
    assert req.headers["Accept"] == "application/json, text/plain;q=0.9"


@responses.activate
def test_get_alarms_with_filters(client):
    responses.add(responses.GET, f"{V1}/alarms", json=ALARM_LIST)
    client.get_alarms(limit=25, offset=10, order_by="lastEventTime",
                      order="descending", severity="MAJOR")
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["25"]
    assert params["offset"] == ["10"]
    assert params["orderBy"] == ["lastEventTime"]
    assert params["order"] == ["descending"]
    assert params["severity"] == ["MAJOR"]


@responses.activate
def test_get_alarm(client):
    responses.add(responses.GET, f"{V1}/alarms/42", json=ALARM)
    result = client.get_alarm(42)
    assert result["id"] == 42
    assert result["severity"] == "MAJOR"
    assert result["uei"] == "uei.opennms.org/nodes/nodeDown"


@responses.activate
def test_get_alarm_count(client):
    responses.add(responses.GET, f"{V1}/alarms/count",
                  body="42", content_type="text/plain")
    result = client.get_alarm_count()
    assert result == 42


@responses.activate
def test_ack_alarm(client):
    responses.add(responses.PUT, f"{V1}/alarms/42", status=204)
    result = client.ack_alarm(42)
    assert result is None
    params = qs(responses.calls[0].request.url)
    assert params["ack"] == ["true"]


@responses.activate
def test_ack_alarm_with_user(client):
    responses.add(responses.PUT, f"{V1}/alarms/42", status=204)
    client.ack_alarm(42, ack_user="jsmith")
    params = qs(responses.calls[0].request.url)
    assert params["ack"] == ["true"]
    assert params["ackUser"] == ["jsmith"]


@responses.activate
def test_unack_alarm(client):
    responses.add(responses.PUT, f"{V1}/alarms/42", status=204)
    result = client.unack_alarm(42)
    assert result is None
    assert qs(responses.calls[0].request.url)["ack"] == ["false"]


@responses.activate
def test_clear_alarm(client):
    responses.add(responses.PUT, f"{V1}/alarms/42", status=204)
    result = client.clear_alarm(42)
    assert result is None
    assert qs(responses.calls[0].request.url)["clear"] == ["true"]


@responses.activate
def test_escalate_alarm(client):
    responses.add(responses.PUT, f"{V1}/alarms/42", status=204)
    result = client.escalate_alarm(42)
    assert result is None
    assert qs(responses.calls[0].request.url)["escalate"] == ["true"]


@responses.activate
def test_bulk_ack_alarms(client):
    responses.add(responses.PUT, f"{V1}/alarms", status=204)
    client.bulk_ack_alarms(severity="MAJOR")
    params = qs(responses.calls[0].request.url)
    assert params["ack"] == ["true"]
    assert params["severity"] == ["MAJOR"]


@responses.activate
def test_bulk_unack_alarms(client):
    responses.add(responses.PUT, f"{V1}/alarms", status=204)
    client.bulk_unack_alarms(nodeLabel="router01.example.com")
    params = qs(responses.calls[0].request.url)
    assert params["ack"] == ["false"]
    assert params["nodeLabel"] == ["router01.example.com"]


@responses.activate
def test_bulk_clear_alarms(client):
    responses.add(responses.PUT, f"{V1}/alarms", status=204)
    client.bulk_clear_alarms(severity="CLEARED")
    assert qs(responses.calls[0].request.url)["clear"] == ["true"]


@responses.activate
def test_bulk_escalate_alarms(client):
    responses.add(responses.PUT, f"{V1}/alarms", status=204)
    client.bulk_escalate_alarms()
    assert qs(responses.calls[0].request.url)["escalate"] == ["true"]


@responses.activate
def test_get_alarms_v2_default(client):
    responses.add(responses.GET, f"{V2}/alarms", json=ALARM_LIST)
    result = client.get_alarms_v2()
    assert result["alarm"][0]["id"] == 42
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["10"]
    assert params["offset"] == ["0"]


@responses.activate
def test_get_alarms_v2_with_fiql(client):
    responses.add(responses.GET, f"{V2}/alarms", json=ALARM_LIST)
    client.get_alarms_v2(fiql="alarm.severity==MAJOR", limit=5)
    params = qs(responses.calls[0].request.url)
    assert params["_s"] == ["alarm.severity==MAJOR"]
    assert params["limit"] == ["5"]


@responses.activate
def test_get_alarm_v2(client):
    responses.add(responses.GET, f"{V2}/alarms/42", json=ALARM)
    result = client.get_alarm_v2(42)
    assert result["id"] == 42
    assert responses.calls[0].request.url.endswith("/api/v2/alarms/42")
