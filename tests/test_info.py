"""Tests for InfoMixin – /rest/info."""
import responses
from .conftest import V1
from .fixtures import SERVER_INFO


@responses.activate
def test_get_info(client):
    responses.add(responses.GET, f"{V1}/info", json=SERVER_INFO)
    result = client.get_info()
    assert result["version"] == "35.0.0"
    assert result["displayVersion"] == "Horizon 35.0.0"
    assert result["packageName"] == "opennms"
    assert result["ticketerConfig"]["enabled"] is False
    assert "OpenNMS:Name=Pollerd" in result["services"]
    assert result["services"]["OpenNMS:Name=Pollerd"] == "running"
    assert responses.calls[0].request.method == "GET"
    assert "/rest/info" in responses.calls[0].request.url
