"""Tests for HeatmapMixin – /rest/heatmap (read-only GET)."""
import responses
from .conftest import V1
from .fixtures import HEATMAP_RESPONSE


def _add(url):
    responses.add(responses.GET, url, json=HEATMAP_RESPONSE)


@responses.activate
def test_get_heatmap_outages_categories(client):
    _add(f"{V1}/heatmap/outages/categories")
    result = client.get_heatmap_outages_categories()
    assert result["heatmapEntry"][0]["label"] == "Production"


@responses.activate
def test_get_heatmap_outages_foreign_sources(client):
    _add(f"{V1}/heatmap/outages/foreignSources")
    result = client.get_heatmap_outages_foreign_sources()
    assert "heatmapEntry" in result


@responses.activate
def test_get_heatmap_outages_monitored_services(client):
    _add(f"{V1}/heatmap/outages/monitoredServices")
    result = client.get_heatmap_outages_monitored_services()
    assert "heatmapEntry" in result


@responses.activate
def test_get_heatmap_outages_nodes_by_category(client):
    _add(f"{V1}/heatmap/outages/nodesByCategory/Production")
    result = client.get_heatmap_outages_nodes_by_category("Production")
    assert "heatmapEntry" in result
    assert "/nodesByCategory/Production" in responses.calls[0].request.url


@responses.activate
def test_get_heatmap_outages_nodes_by_foreign_source(client):
    _add(f"{V1}/heatmap/outages/nodesByForeignSource/Routers")
    result = client.get_heatmap_outages_nodes_by_foreign_source("Routers")
    assert "heatmapEntry" in result


@responses.activate
def test_get_heatmap_outages_nodes_by_service(client):
    _add(f"{V1}/heatmap/outages/nodesByMonitoredService/ICMP")
    result = client.get_heatmap_outages_nodes_by_service("ICMP")
    assert "heatmapEntry" in result


@responses.activate
def test_get_heatmap_alarms_categories(client):
    _add(f"{V1}/heatmap/alarms/categories")
    result = client.get_heatmap_alarms_categories()
    assert result["heatmapEntry"][0]["maximumSeverity"] == "MAJOR"


@responses.activate
def test_get_heatmap_alarms_foreign_sources(client):
    _add(f"{V1}/heatmap/alarms/foreignSources")
    result = client.get_heatmap_alarms_foreign_sources()
    assert "heatmapEntry" in result


@responses.activate
def test_get_heatmap_alarms_monitored_services(client):
    _add(f"{V1}/heatmap/alarms/monitoredServices")
    result = client.get_heatmap_alarms_monitored_services()
    assert "heatmapEntry" in result


@responses.activate
def test_get_heatmap_alarms_nodes_by_category(client):
    _add(f"{V1}/heatmap/alarms/nodesByCategory/Production")
    result = client.get_heatmap_alarms_nodes_by_category("Production")
    assert "heatmapEntry" in result
    assert "/alarms/nodesByCategory/Production" in responses.calls[0].request.url


@responses.activate
def test_get_heatmap_alarms_nodes_by_foreign_source(client):
    _add(f"{V1}/heatmap/alarms/nodesByForeignSource/Routers")
    result = client.get_heatmap_alarms_nodes_by_foreign_source("Routers")
    assert "heatmapEntry" in result


@responses.activate
def test_get_heatmap_alarms_nodes_by_service(client):
    _add(f"{V1}/heatmap/alarms/nodesByMonitoredService/ICMP")
    result = client.get_heatmap_alarms_nodes_by_service("ICMP")
    assert "heatmapEntry" in result
