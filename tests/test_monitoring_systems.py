"""Tests for MonitoringSystemsMixin – /rest/monitoringSystems."""
import responses
from .conftest import V1
from .fixtures import MONITORING_SYSTEM


@responses.activate
def test_get_monitoring_system(client):
    responses.add(responses.GET, f"{V1}/monitoringSystems/main",
                  json=MONITORING_SYSTEM)
    result = client.get_monitoring_system()
    assert result["type"] == "OpenNMS"
    assert result["location"] == "Default"
