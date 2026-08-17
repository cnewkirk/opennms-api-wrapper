"""Tests for GrafanaEndpointsMixin – /rest/endpoints/grafana."""
import json

import responses
from .conftest import V1
from .fixtures import (
    GRAFANA_ENDPOINT, GRAFANA_ENDPOINT_LIST, GRAFANA_DASHBOARD,
    GRAFANA_DASHBOARD_LIST,
)


@responses.activate
def test_get_grafana_endpoints(client):
    responses.add(responses.GET, f"{V1}/endpoints/grafana",
                  json=GRAFANA_ENDPOINT_LIST)
    result = client.get_grafana_endpoints()
    assert result[0]["url"] == "https://grafana.example.com"


@responses.activate
def test_get_grafana_endpoints_empty(client):
    responses.add(responses.GET, f"{V1}/endpoints/grafana",
                  status=204)
    assert client.get_grafana_endpoints() is None


@responses.activate
def test_get_grafana_endpoint(client):
    responses.add(responses.GET, f"{V1}/endpoints/grafana/1",
                  json=GRAFANA_ENDPOINT)
    assert client.get_grafana_endpoint(1)["id"] == 1


@responses.activate
def test_get_grafana_dashboards(client):
    uid = GRAFANA_ENDPOINT["uid"]
    responses.add(responses.GET,
                  f"{V1}/endpoints/grafana/{uid}/dashboards",
                  json=GRAFANA_DASHBOARD_LIST)
    result = client.get_grafana_dashboards(uid)
    assert result[0]["title"] == "Node performance"


@responses.activate
def test_get_grafana_dashboard(client):
    uid = GRAFANA_ENDPOINT["uid"]
    responses.add(
        responses.GET,
        f"{V1}/endpoints/grafana/{uid}/dashboards/b0d92dk4z",
        json=GRAFANA_DASHBOARD)
    result = client.get_grafana_dashboard(uid, "b0d92dk4z")
    assert result["uid"] == "b0d92dk4z"


@responses.activate
def test_create_grafana_endpoint(client):
    responses.add(responses.POST, f"{V1}/endpoints/grafana",
                  status=202)
    client.create_grafana_endpoint(GRAFANA_ENDPOINT)
    body = json.loads(responses.calls[0].request.body)
    assert body["uid"] == GRAFANA_ENDPOINT["uid"]


@responses.activate
def test_verify_grafana_endpoint(client):
    responses.add(responses.POST, f"{V1}/endpoints/grafana/verify",
                  status=200)
    client.verify_grafana_endpoint(
        {"url": "https://grafana.example.com", "apiKey": "abc"})
    body = json.loads(responses.calls[0].request.body)
    assert body["apiKey"] == "abc"


@responses.activate
def test_update_grafana_endpoint(client):
    responses.add(responses.PUT, f"{V1}/endpoints/grafana/1",
                  status=202)
    client.update_grafana_endpoint(1, GRAFANA_ENDPOINT)
    body = json.loads(responses.calls[0].request.body)
    assert body["id"] == 1


@responses.activate
def test_delete_grafana_endpoints(client):
    responses.add(responses.DELETE, f"{V1}/endpoints/grafana",
                  status=202)
    assert client.delete_grafana_endpoints() is None


@responses.activate
def test_delete_grafana_endpoint(client):
    responses.add(responses.DELETE, f"{V1}/endpoints/grafana/1",
                  status=202)
    assert client.delete_grafana_endpoint(1) is None
