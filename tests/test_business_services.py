"""Tests for BusinessServicesMixin – /api/v2/business-services."""
import json
import responses
from .conftest import V2
from .fixtures import BUSINESS_SERVICE, BUSINESS_SERVICE_LIST


@responses.activate
def test_get_business_services(client):
    responses.add(responses.GET, f"{V2}/business-services",
                  json=BUSINESS_SERVICE_LIST)
    result = client.get_business_services()
    assert result["business-services"][0]["id"] == 1001
    assert result["business-services"][0]["name"] == "Core Network Availability"


@responses.activate
def test_get_business_service(client):
    responses.add(responses.GET, f"{V2}/business-services/1001",
                  json=BUSINESS_SERVICE)
    result = client.get_business_service(1001)
    assert result["id"] == 1001
    assert result["operationalStatus"] == "MAJOR"
    assert len(result["edges"]) == 1
    assert "/business-services/1001" in responses.calls[0].request.url


@responses.activate
def test_create_business_service(client):
    responses.add(responses.POST, f"{V2}/business-services",
                  json=BUSINESS_SERVICE, status=201)
    payload = {
        "name": "Core Network Availability",
        "attributes": {"dc": "us-east-1", "tier": "critical"},
        "reduceFunction": {"type": "HighestSeverity"},
    }
    result = client.create_business_service(payload)
    assert result["id"] == 1001
    req = responses.calls[0].request
    body = json.loads(req.body)
    assert body["name"] == "Core Network Availability"
    assert body["reduceFunction"]["type"] == "HighestSeverity"
    assert req.headers["Content-Type"] == "application/json"


@responses.activate
def test_update_business_service(client):
    responses.add(responses.PUT, f"{V2}/business-services/1001",
                  status=204)
    updated = {**BUSINESS_SERVICE, "name": "Renamed Service"}
    result = client.update_business_service(1001, updated)
    assert result is None
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "Renamed Service"
    assert "/business-services/1001" in responses.calls[0].request.url


@responses.activate
def test_delete_business_service(client):
    responses.add(responses.DELETE, f"{V2}/business-services/1001",
                  status=204)
    result = client.delete_business_service(1001)
    assert result is None
    assert responses.calls[0].request.method == "DELETE"
    assert "/business-services/1001" in responses.calls[0].request.url
