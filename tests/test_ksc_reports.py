"""Tests for KscReportsMixin – /rest/ksc."""
import json
import responses
from .conftest import V1
from .fixtures import KSC_REPORT, KSC_REPORT_LIST


@responses.activate
def test_get_ksc_reports(client):
    responses.add(responses.GET, f"{V1}/ksc", json=KSC_REPORT_LIST)
    result = client.get_ksc_reports()
    assert result["kscReport"][0]["id"] == 1
    assert result["kscReport"][0]["label"] == "Core Bandwidth Report"


@responses.activate
def test_get_ksc_report(client):
    responses.add(responses.GET, f"{V1}/ksc/1", json=KSC_REPORT)
    result = client.get_ksc_report(1)
    assert result["id"] == 1
    assert result["label"] == "Core Bandwidth Report"
    assert len(result["graphs"]) == 1
    assert result["graphs"][0]["timespan"] == "7_day"


@responses.activate
def test_get_ksc_report_count(client):
    responses.add(responses.GET, f"{V1}/ksc/count",
                  body="5", content_type="text/plain")
    assert client.get_ksc_report_count() == 5


@responses.activate
def test_create_ksc_report(client):
    responses.add(responses.POST, f"{V1}/ksc", json=KSC_REPORT, status=201)
    client.create_ksc_report(KSC_REPORT)
    body = json.loads(responses.calls[0].request.body)
    assert body["label"] == "Core Bandwidth Report"
    assert body["graphs"][0]["graphtype"] == "mib2.bits"
    assert responses.calls[0].request.headers["Content-Type"] == "application/json"


@responses.activate
def test_update_ksc_report(client):
    responses.add(responses.PUT, f"{V1}/ksc/1", status=204)
    client.update_ksc_report(1, {**KSC_REPORT, "label": "Updated Report"})
    body = json.loads(responses.calls[0].request.body)
    assert body["label"] == "Updated Report"
