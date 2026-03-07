"""Tests for ForeignSourcesMixin – /rest/foreignSources."""
import json
import responses
from .conftest import V1
from .fixtures import (
    FOREIGN_SOURCE, FOREIGN_SOURCE_LIST,
    FOREIGN_SOURCE_DETECTOR, FOREIGN_SOURCE_POLICY,
)


@responses.activate
def test_get_foreign_sources(client):
    responses.add(responses.GET, f"{V1}/foreignSources",
                  json=FOREIGN_SOURCE_LIST)
    result = client.get_foreign_sources()
    assert result["foreignSource"][0]["name"] == "Routers"


@responses.activate
def test_get_foreign_source(client):
    responses.add(responses.GET, f"{V1}/foreignSources/Routers",
                  json=FOREIGN_SOURCE)
    result = client.get_foreign_source("Routers")
    assert result["name"] == "Routers"
    assert result["scan-interval"] == "1d"


@responses.activate
def test_get_default_foreign_source(client):
    responses.add(responses.GET, f"{V1}/foreignSources/default",
                  json=FOREIGN_SOURCE)
    result = client.get_default_foreign_source()
    assert result["name"] == "Routers"
    assert "/foreignSources/default" in responses.calls[0].request.url


@responses.activate
def test_get_deployed_foreign_sources(client):
    responses.add(responses.GET, f"{V1}/foreignSources/deployed",
                  json=FOREIGN_SOURCE_LIST)
    result = client.get_deployed_foreign_sources()
    assert result["foreignSource"][0]["name"] == "Routers"


@responses.activate
def test_get_deployed_foreign_source_count(client):
    responses.add(responses.GET, f"{V1}/foreignSources/deployed/count",
                  body="4", content_type="text/plain")
    assert client.get_deployed_foreign_source_count() == 4


@responses.activate
def test_create_foreign_source(client):
    responses.add(responses.POST, f"{V1}/foreignSources",
                  json=FOREIGN_SOURCE, status=200)
    client.create_foreign_source(FOREIGN_SOURCE)
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "Routers"
    assert responses.calls[0].request.headers["Content-Type"] == "application/json"


@responses.activate
def test_update_foreign_source(client):
    responses.add(responses.PUT, f"{V1}/foreignSources/Routers",
                  status=204)
    client.update_foreign_source("Routers", {**FOREIGN_SOURCE, "scan-interval": "12h"})
    body = json.loads(responses.calls[0].request.body)
    assert body["scan-interval"] == "12h"


@responses.activate
def test_delete_foreign_source(client):
    responses.add(responses.DELETE, f"{V1}/foreignSources/Routers", status=202)
    result = client.delete_foreign_source("Routers")
    assert result is None


@responses.activate
def test_get_foreign_source_detectors(client):
    responses.add(responses.GET, f"{V1}/foreignSources/Routers/detectors",
                  json={"detector": [FOREIGN_SOURCE_DETECTOR]})
    result = client.get_foreign_source_detectors("Routers")
    assert result["detector"][0]["name"] == "ICMP"


@responses.activate
def test_get_foreign_source_detector(client):
    responses.add(responses.GET, f"{V1}/foreignSources/Routers/detectors/ICMP",
                  json=FOREIGN_SOURCE_DETECTOR)
    result = client.get_foreign_source_detector("Routers", "ICMP")
    assert result["class"].endswith("IcmpDetector")


@responses.activate
def test_add_foreign_source_detector(client):
    responses.add(responses.POST, f"{V1}/foreignSources/Routers/detectors",
                  json=FOREIGN_SOURCE_DETECTOR, status=200)
    client.add_foreign_source_detector("Routers", FOREIGN_SOURCE_DETECTOR)
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "ICMP"


@responses.activate
def test_delete_foreign_source_detector(client):
    responses.add(responses.DELETE,
                  f"{V1}/foreignSources/Routers/detectors/ICMP",
                  status=204)
    result = client.delete_foreign_source_detector("Routers", "ICMP")
    assert result is None


@responses.activate
def test_get_foreign_source_policies(client):
    responses.add(responses.GET, f"{V1}/foreignSources/Routers/policies",
                  json={"policy": [FOREIGN_SOURCE_POLICY]})
    result = client.get_foreign_source_policies("Routers")
    assert result["policy"][0]["name"] == "Do Not Persist Discovered IPs"


@responses.activate
def test_get_foreign_source_policy(client):
    # requests percent-encodes spaces in path segments as %20, not +
    encoded = "Do%20Not%20Persist%20Discovered%20IPs"
    responses.add(responses.GET,
                  f"{V1}/foreignSources/Routers/policies/{encoded}",
                  json=FOREIGN_SOURCE_POLICY)
    result = client.get_foreign_source_policy(
        "Routers", "Do Not Persist Discovered IPs")
    assert result["name"] == "Do Not Persist Discovered IPs"


@responses.activate
def test_add_foreign_source_policy(client):
    responses.add(responses.POST, f"{V1}/foreignSources/Routers/policies",
                  json=FOREIGN_SOURCE_POLICY, status=200)
    client.add_foreign_source_policy("Routers", FOREIGN_SOURCE_POLICY)
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "Do Not Persist Discovered IPs"


@responses.activate
def test_delete_foreign_source_policy(client):
    encoded = "Do%20Not%20Persist%20Discovered%20IPs"
    responses.add(responses.DELETE,
                  f"{V1}/foreignSources/Routers/policies/{encoded}",
                  status=204)
    result = client.delete_foreign_source_policy(
        "Routers", "Do Not Persist Discovered IPs")
    assert result is None
