"""Tests for AlarmStatsMixin – /rest/stats/alarms."""
import responses
from .conftest import V1, qs
from .fixtures import ALARM_STATS, ALARM_STATS_BY_SEVERITY


@responses.activate
def test_get_alarm_stats(client):
    responses.add(responses.GET, f"{V1}/stats/alarms", json=ALARM_STATS)
    result = client.get_alarm_stats()
    assert result["totalCount"] == 15
    assert result["acknowledgedCount"] == 5


@responses.activate
def test_get_alarm_stats_with_filters(client):
    responses.add(responses.GET, f"{V1}/stats/alarms", json=ALARM_STATS)
    client.get_alarm_stats(severity="MAJOR")
    assert qs(responses.calls[0].request.url)["severity"] == ["MAJOR"]


@responses.activate
def test_get_alarm_stats_by_severity(client):
    responses.add(responses.GET, f"{V1}/stats/alarms/by-severity",
                  json=ALARM_STATS_BY_SEVERITY)
    result = client.get_alarm_stats_by_severity()
    assert isinstance(result, list)
    assert result[0]["severity"] == "CRITICAL"


@responses.activate
def test_get_alarm_stats_by_severity_filtered(client):
    responses.add(responses.GET, f"{V1}/stats/alarms/by-severity",
                  json=ALARM_STATS_BY_SEVERITY[:2])
    client.get_alarm_stats_by_severity(severities=["CRITICAL", "MAJOR"])
    assert qs(responses.calls[0].request.url)["severities"] == ["CRITICAL,MAJOR"]
