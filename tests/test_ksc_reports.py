"""Tests for KscReportsMixin – /rest/ksc."""
import responses
from .conftest import V1, XML, add_contract, qs
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
    add_contract(responses.POST, f"{V1}/ksc", XML, status=303)
    client.create_ksc_report(KSC_REPORT)
    body = responses.calls[0].request.body
    assert body.startswith(
        '<kscReport id="1" label="Core Bandwidth Report"'
        ' show_timespan_button="true" show_graphtype_button="false"'
        ' graphs_per_line="2">')
    assert '<kscGraph title="Core Switch Bandwidth"' in body
    assert 'graphtype="mib2.bits"' in body


@responses.activate
def test_add_graph_to_ksc_report(client):
    responses.add(responses.PUT, f"{V1}/ksc/1", status=303)
    client.add_graph_to_ksc_report(
        1, "mib2.bits", "node[1].interfaceSnmp[eth0]",
        title="Bandwidth", timespan="7_day")
    params = qs(responses.calls[0].request.url)
    assert params["reportName"] == ["mib2.bits"]
    assert params["resourceId"] == ["node[1].interfaceSnmp[eth0]"]
    assert params["title"] == ["Bandwidth"]
    assert params["timespan"] == ["7_day"]
