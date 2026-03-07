"""Tests for AlarmHistoryMixin – /rest/alarms/history."""
import responses
from .conftest import V1, qs
from .fixtures import ALARM_HISTORY_LIST, ALARM_HISTORY_STATE, ALARM_HISTORY_STATES_LIST


@responses.activate
def test_get_alarm_history(client):
    responses.add(responses.GET, f"{V1}/alarms/history", json=ALARM_HISTORY_LIST)
    result = client.get_alarm_history()
    assert isinstance(result, list)
    assert result[0]["id"] == 42


@responses.activate
def test_get_alarm_history_with_timestamp(client):
    responses.add(responses.GET, f"{V1}/alarms/history", json=ALARM_HISTORY_LIST)
    client.get_alarm_history(at=1717228800000)
    assert qs(responses.calls[0].request.url)["at"] == ["1717228800000"]


@responses.activate
def test_get_alarm_history_at(client):
    responses.add(responses.GET, f"{V1}/alarms/history/42", json=ALARM_HISTORY_STATE)
    result = client.get_alarm_history_at(42)
    assert result["alarmId"] == 42
    assert result["type"] == "ALARM_CREATED"


@responses.activate
def test_get_alarm_history_at_with_timestamp(client):
    responses.add(responses.GET, f"{V1}/alarms/history/42", json=ALARM_HISTORY_STATE)
    client.get_alarm_history_at(42, at=1717228800000)
    assert qs(responses.calls[0].request.url)["at"] == ["1717228800000"]


@responses.activate
def test_get_alarm_history_states(client):
    responses.add(responses.GET, f"{V1}/alarms/history/42/states",
                  json=ALARM_HISTORY_STATES_LIST)
    result = client.get_alarm_history_states(42)
    assert isinstance(result, list)
    assert result[0]["alarmId"] == 42
    assert responses.calls[0].request.url.endswith("/alarms/history/42/states")
