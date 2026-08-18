"""Tests for ReportsMixin – /rest/reports."""
import json

import responses
from .conftest import V1, qs
from .fixtures import (
    REPORT_TEMPLATE_LIST, REPORT_TEMPLATE_DETAILS, REPORT_PDF,
    PERSISTED_REPORT_LIST, SCHEDULED_REPORT, SCHEDULED_REPORT_LIST,
)


@responses.activate
def test_get_report_templates(client):
    responses.add(responses.GET, f"{V1}/reports",
                  json=REPORT_TEMPLATE_LIST)
    result = client.get_report_templates()
    assert result[0]["id"] == "local_Early-Morning-Report"


@responses.activate
def test_get_report_template(client):
    responses.add(responses.GET,
                  f"{V1}/reports/local_Early-Morning-Report",
                  json=REPORT_TEMPLATE_DETAILS)
    result = client.get_report_template("local_Early-Morning-Report",
                                        user_id="admin")
    assert result["formats"][0]["name"] == "PDF"
    assert qs(responses.calls[0].request.url)["userId"] == ["admin"]


@responses.activate
def test_run_report(client):
    responses.add(responses.POST,
                  f"{V1}/reports/local_Early-Morning-Report",
                  body=REPORT_PDF, content_type="application/pdf")
    params = [{"name": "range", "type": "date",
               "value": "2026-08-01"}]
    result = client.run_report("local_Early-Morning-Report", "PDF",
                               params)
    assert result == REPORT_PDF
    body = json.loads(responses.calls[0].request.body)
    assert body["format"] == "PDF"
    assert body["parameters"] == params


@responses.activate
def test_get_persisted_reports(client):
    responses.add(responses.GET, f"{V1}/reports/persisted",
                  json=PERSISTED_REPORT_LIST)
    result = client.get_persisted_reports()
    assert result[0]["id"] == 1


@responses.activate
def test_deliver_report(client):
    responses.add(responses.POST, f"{V1}/reports/persisted",
                  status=202)
    client.deliver_report(
        "local_Early-Morning-Report", "PDF", [],
        {"instanceId": "morning", "persist": True})
    body = json.loads(responses.calls[0].request.body)
    assert body["id"] == "local_Early-Morning-Report"
    assert body["deliveryOptions"]["persist"] is True


@responses.activate
def test_download_report(client):
    responses.add(responses.GET, f"{V1}/reports/download",
                  body=REPORT_PDF, content_type="application/pdf")
    result = client.download_report(1, format="PDF")
    assert result == REPORT_PDF
    params = qs(responses.calls[0].request.url)
    assert params["locatorId"] == ["1"]
    assert params["format"] == ["PDF"]


@responses.activate
def test_delete_persisted_reports(client):
    responses.add(responses.DELETE, f"{V1}/reports/persisted",
                  status=202)
    assert client.delete_persisted_reports() is None


@responses.activate
def test_delete_persisted_report(client):
    responses.add(responses.DELETE, f"{V1}/reports/persisted/1",
                  status=202)
    assert client.delete_persisted_report(1) is None


@responses.activate
def test_get_scheduled_reports(client):
    responses.add(responses.GET, f"{V1}/reports/scheduled",
                  json=SCHEDULED_REPORT_LIST)
    result = client.get_scheduled_reports()
    assert result[0]["triggerName"] == "report_trigger_1"


@responses.activate
def test_get_scheduled_report(client):
    responses.add(responses.GET,
                  f"{V1}/reports/scheduled/report_trigger_1",
                  json=SCHEDULED_REPORT)
    result = client.get_scheduled_report("report_trigger_1")
    assert result["cronExpression"] == "0 0 6 * * ?"


@responses.activate
def test_schedule_report(client):
    responses.add(responses.POST, f"{V1}/reports/scheduled",
                  status=202)
    client.schedule_report(
        "local_Early-Morning-Report", "PDF", "0 0 6 * * ?", [],
        {"instanceId": "morning", "sendMail": True,
         "mailTo": "noc@example.com"})
    body = json.loads(responses.calls[0].request.body)
    assert body["cronExpression"] == "0 0 6 * * ?"
    assert body["deliveryOptions"]["mailTo"] == "noc@example.com"


@responses.activate
def test_update_scheduled_report(client):
    responses.add(responses.PUT,
                  f"{V1}/reports/scheduled/report_trigger_1",
                  status=202)
    client.update_scheduled_report(
        "report_trigger_1", {"cronExpression": "0 0 7 * * ?"})
    body = json.loads(responses.calls[0].request.body)
    assert body["cronExpression"] == "0 0 7 * * ?"


@responses.activate
def test_delete_scheduled_reports(client):
    responses.add(responses.DELETE, f"{V1}/reports/scheduled",
                  status=202)
    assert client.delete_scheduled_reports() is None


@responses.activate
def test_delete_scheduled_report(client):
    responses.add(responses.DELETE,
                  f"{V1}/reports/scheduled/report_trigger_1",
                  status=202)
    assert client.delete_scheduled_report("report_trigger_1") is None
