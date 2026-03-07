"""Tests for ConfigMgmtMixin – /rest/cm."""
import json
import responses
from .conftest import V1
from .fixtures import CONFIG_NAMES, CONFIG_SCHEMAS, CONFIG_SCHEMA, CONFIG_IDS, CONFIG


@responses.activate
def test_get_config_names(client):
    responses.add(responses.GET, f"{V1}/cm", json=CONFIG_NAMES)
    result = client.get_config_names()
    assert "provisiond" in result


@responses.activate
def test_get_config_schemas(client):
    responses.add(responses.GET, f"{V1}/cm/schema", json=CONFIG_SCHEMAS)
    result = client.get_config_schemas()
    assert result["schema"][0]["name"] == "provisiond"


@responses.activate
def test_get_config_schema(client):
    responses.add(responses.GET, f"{V1}/cm/schema/provisiond",
                  json=CONFIG_SCHEMA)
    result = client.get_config_schema("provisiond")
    assert result["name"] == "provisiond"


@responses.activate
def test_get_config_ids(client):
    responses.add(responses.GET, f"{V1}/cm/provisiond", json=CONFIG_IDS)
    result = client.get_config_ids("provisiond")
    assert "default" in result


@responses.activate
def test_get_config(client):
    responses.add(responses.GET, f"{V1}/cm/provisiond/default",
                  json=CONFIG)
    result = client.get_config("provisiond", "default")
    assert result["name"] == "provisiond"


@responses.activate
def test_get_config_part(client):
    responses.add(responses.GET,
                  f"{V1}/cm/provisiond/default/importThreads",
                  json={"value": 8})
    result = client.get_config_part("provisiond", "default",
                                    "importThreads")
    assert result["value"] == 8


@responses.activate
def test_create_config(client):
    responses.add(responses.POST, f"{V1}/cm/provisiond/default",
                  status=201)
    client.create_config("provisiond", "default",
                         {"importThreads": 8})
    body = json.loads(responses.calls[0].request.body)
    assert body["importThreads"] == 8


@responses.activate
def test_update_config(client):
    responses.add(responses.PUT, f"{V1}/cm/provisiond/default",
                  status=204)
    result = client.update_config("provisiond", "default",
                                  {"importThreads": 16})
    assert result is None


@responses.activate
def test_delete_config(client):
    responses.add(responses.DELETE, f"{V1}/cm/provisiond/default",
                  status=204)
    result = client.delete_config("provisiond", "default")
    assert result is None


@responses.activate
def test_delete_config_part(client):
    responses.add(responses.DELETE,
                  f"{V1}/cm/provisiond/default/importThreads",
                  status=204)
    result = client.delete_config_part("provisiond", "default",
                                       "importThreads")
    assert result is None
