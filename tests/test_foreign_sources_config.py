"""Tests for ForeignSourcesConfigMixin – /rest/foreignSourcesConfig."""
import responses
from .conftest import V1
from .fixtures import (
    FS_CONFIG_POLICIES, FS_CONFIG_DETECTORS, FS_CONFIG_SERVICES,
    FS_CONFIG_ASSETS, FS_CONFIG_CATEGORIES,
)


@responses.activate
def test_get_foreign_source_config_policies(client):
    responses.add(responses.GET, f"{V1}/foreignSourcesConfig/policies",
                  json=FS_CONFIG_POLICIES)
    result = client.get_foreign_source_config_policies()
    assert result["plugin"][0]["name"] == "Match IP Interface"


@responses.activate
def test_get_foreign_source_config_detectors(client):
    responses.add(responses.GET, f"{V1}/foreignSourcesConfig/detectors",
                  json=FS_CONFIG_DETECTORS)
    result = client.get_foreign_source_config_detectors()
    assert result["plugin"][0]["name"] == "ICMP"


@responses.activate
def test_get_foreign_source_config_services(client):
    responses.add(responses.GET,
                  f"{V1}/foreignSourcesConfig/services/Routers",
                  json=FS_CONFIG_SERVICES)
    result = client.get_foreign_source_config_services("Routers")
    assert "ICMP" in result["service"]


@responses.activate
def test_get_foreign_source_config_assets(client):
    responses.add(responses.GET, f"{V1}/foreignSourcesConfig/assets",
                  json=FS_CONFIG_ASSETS)
    result = client.get_foreign_source_config_assets()
    assert "manufacturer" in result["asset"]


@responses.activate
def test_get_foreign_source_config_categories(client):
    responses.add(responses.GET,
                  f"{V1}/foreignSourcesConfig/categories",
                  json=FS_CONFIG_CATEGORIES)
    result = client.get_foreign_source_config_categories()
    assert "Production" in result["category"]
