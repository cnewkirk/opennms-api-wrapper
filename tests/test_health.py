"""Tests for HealthMixin – /rest/health."""
import responses
from .conftest import V1, qs
from .fixtures import HEALTH, HEALTH_PROBE


@responses.activate
def test_get_health(client):
    responses.add(responses.GET, f"{V1}/health", json=HEALTH)
    result = client.get_health()
    assert result["healthy"] is True


@responses.activate
def test_get_health_with_tag(client):
    responses.add(responses.GET, f"{V1}/health", json=HEALTH)
    client.get_health(tag="bundle")
    assert qs(responses.calls[0].request.url)["tag"] == ["bundle"]


@responses.activate
def test_get_health_probe(client):
    responses.add(responses.GET, f"{V1}/health/probe", json=HEALTH_PROBE)
    result = client.get_health_probe()
    assert "awesome" in result["status"]
