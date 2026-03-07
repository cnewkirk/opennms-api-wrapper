"""Tests for DiscoveryMixin – /api/v2/discovery."""
import json
import responses
from .conftest import V2


@responses.activate
def test_discover_specifics(client):
    responses.add(responses.POST, f"{V2}/discovery", status=204)
    config = {
        "specifics": [
            {
                "ip": "10.0.0.1",
                "location": "Default",
                "retries": 1,
                "timeout": 2000,
                "foreignSource": "Routers",
            }
        ]
    }
    result = client.discover(config)
    assert result is None
    req = responses.calls[0].request
    assert req.method == "POST"
    assert "/api/v2/discovery" in req.url
    body = json.loads(req.body)
    assert body["specifics"][0]["ip"] == "10.0.0.1"
    assert body["specifics"][0]["foreignSource"] == "Routers"
    assert req.headers["Content-Type"] == "application/json"


@responses.activate
def test_discover_with_ranges(client):
    responses.add(responses.POST, f"{V2}/discovery", status=204)
    config = {
        "include_ranges": [
            {"begin": "10.0.1.1", "end": "10.0.1.254",
             "location": "Default", "retries": 1, "timeout": 2000}
        ],
        "exclude_ranges": [
            {"begin": "10.0.1.100", "end": "10.0.1.110"}
        ],
    }
    result = client.discover(config)
    assert result is None
    body = json.loads(responses.calls[0].request.body)
    assert body["include_ranges"][0]["begin"] == "10.0.1.1"
    assert body["exclude_ranges"][0]["end"] == "10.0.1.110"


@responses.activate
def test_discover_with_url(client):
    responses.add(responses.POST, f"{V2}/discovery", status=204)
    config = {
        "include_urls": [
            {"url": "file:/opt/opennms/etc/include.txt",
             "location": "Default"}
        ]
    }
    result = client.discover(config)
    assert result is None
    body = json.loads(responses.calls[0].request.body)
    assert body["include_urls"][0]["location"] == "Default"
