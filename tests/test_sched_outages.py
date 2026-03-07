"""Tests for SchedOutagesMixin – /rest/sched-outages."""
import json
import responses
from .conftest import V1
from .fixtures import SCHED_OUTAGE, SCHED_OUTAGE_LIST


@responses.activate
def test_get_sched_outages(client):
    responses.add(responses.GET, f"{V1}/sched-outages", json=SCHED_OUTAGE_LIST)
    result = client.get_sched_outages()
    assert result["scheduleOutage"][0]["name"] == "Weekend-Maintenance"


@responses.activate
def test_get_sched_outage(client):
    responses.add(responses.GET, f"{V1}/sched-outages/Weekend-Maintenance",
                  json=SCHED_OUTAGE)
    result = client.get_sched_outage("Weekend-Maintenance")
    assert result["name"] == "Weekend-Maintenance"
    assert result["type"] == "weekly"
    assert len(result["time"]) == 2


@responses.activate
def test_create_sched_outage(client):
    responses.add(responses.POST, f"{V1}/sched-outages",
                  json=SCHED_OUTAGE, status=200)
    client.create_sched_outage(SCHED_OUTAGE)
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "Weekend-Maintenance"
    assert body["type"] == "weekly"
    assert responses.calls[0].request.headers["Content-Type"] == "application/json"


@responses.activate
def test_delete_sched_outage(client):
    responses.add(responses.DELETE, f"{V1}/sched-outages/Weekend-Maintenance",
                  status=204)
    result = client.delete_sched_outage("Weekend-Maintenance")
    assert result is None


@responses.activate
def test_associate_sched_outage_collectd(client):
    responses.add(responses.PUT,
                  f"{V1}/sched-outages/Weekend-Maintenance/collectd/default",
                  status=204)
    result = client.associate_sched_outage_collectd("Weekend-Maintenance", "default")
    assert result is None


@responses.activate
def test_dissociate_sched_outage_collectd(client):
    responses.add(responses.DELETE,
                  f"{V1}/sched-outages/Weekend-Maintenance/collectd/default",
                  status=204)
    result = client.dissociate_sched_outage_collectd("Weekend-Maintenance", "default")
    assert result is None


@responses.activate
def test_associate_sched_outage_pollerd(client):
    responses.add(responses.PUT,
                  f"{V1}/sched-outages/Weekend-Maintenance/pollerd/example1",
                  status=204)
    result = client.associate_sched_outage_pollerd("Weekend-Maintenance", "example1")
    assert result is None


@responses.activate
def test_dissociate_sched_outage_pollerd(client):
    responses.add(responses.DELETE,
                  f"{V1}/sched-outages/Weekend-Maintenance/pollerd/example1",
                  status=204)
    result = client.dissociate_sched_outage_pollerd("Weekend-Maintenance", "example1")
    assert result is None


@responses.activate
def test_associate_sched_outage_threshd(client):
    responses.add(responses.PUT,
                  f"{V1}/sched-outages/Weekend-Maintenance/threshd/default",
                  status=204)
    result = client.associate_sched_outage_threshd("Weekend-Maintenance", "default")
    assert result is None


@responses.activate
def test_dissociate_sched_outage_threshd(client):
    responses.add(responses.DELETE,
                  f"{V1}/sched-outages/Weekend-Maintenance/threshd/default",
                  status=204)
    result = client.dissociate_sched_outage_threshd("Weekend-Maintenance", "default")
    assert result is None


@responses.activate
def test_associate_sched_outage_notifd(client):
    responses.add(responses.PUT,
                  f"{V1}/sched-outages/Weekend-Maintenance/notifd",
                  status=204)
    result = client.associate_sched_outage_notifd("Weekend-Maintenance")
    assert result is None


@responses.activate
def test_dissociate_sched_outage_notifd(client):
    responses.add(responses.DELETE,
                  f"{V1}/sched-outages/Weekend-Maintenance/notifd",
                  status=204)
    result = client.dissociate_sched_outage_notifd("Weekend-Maintenance")
    assert result is None
