"""Tests for StatusMixin – /api/v2/status."""
import responses
from .conftest import V2, qs
from .fixtures import (
    STATUS_SUMMARY, STATUS_NODE_LIST, STATUS_APPLICATION_LIST,
    STATUS_BUSINESS_SERVICE_LIST,
)


@responses.activate
def test_get_status_summary_nodes(client):
    responses.add(responses.GET, f"{V2}/status/summary/nodes/alarms",
                  json=STATUS_SUMMARY)
    result = client.get_status_summary_nodes()
    assert result == STATUS_SUMMARY


@responses.activate
def test_get_status_summary_nodes_outages(client):
    responses.add(responses.GET, f"{V2}/status/summary/nodes/outages",
                  json=STATUS_SUMMARY)
    result = client.get_status_summary_nodes(type="outages")
    assert result[0] == ["Normal", 42]


@responses.activate
def test_get_status_summary_applications(client):
    responses.add(responses.GET,
                  f"{V2}/status/summary/applications",
                  json=STATUS_SUMMARY)
    assert client.get_status_summary_applications() == STATUS_SUMMARY


@responses.activate
def test_get_status_summary_business_services(client):
    responses.add(responses.GET,
                  f"{V2}/status/summary/business-services",
                  json=STATUS_SUMMARY)
    result = client.get_status_summary_business_services()
    assert result == STATUS_SUMMARY


@responses.activate
def test_get_status_nodes(client):
    responses.add(responses.GET, f"{V2}/status/nodes/alarms",
                  json=STATUS_NODE_LIST)
    result = client.get_status_nodes(limit=10, offset=0,
                                     severity_filter="CRITICAL")
    assert result["totalCount"] == 1
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["10"]
    assert params["severityFilter"] == ["CRITICAL"]


@responses.activate
def test_get_status_applications(client):
    responses.add(responses.GET, f"{V2}/status/applications",
                  json=STATUS_APPLICATION_LIST)
    result = client.get_status_applications(order_by="severity",
                                            order="desc")
    assert result["applications"][0]["name"] == "Customer Portal"
    params = qs(responses.calls[0].request.url)
    assert params["orderBy"] == ["severity"]
    assert params["order"] == ["desc"]


@responses.activate
def test_get_status_business_services(client):
    responses.add(responses.GET, f"{V2}/status/business-services",
                  json=STATUS_BUSINESS_SERVICE_LIST)
    result = client.get_status_business_services()
    assert result["business-services"][0]["name"] == "Email"
    assert "?" not in responses.calls[0].request.url
