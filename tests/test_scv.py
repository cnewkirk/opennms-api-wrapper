"""Tests for ScvMixin – /rest/scv."""
import json
import responses
from .conftest import V1
from .fixtures import CREDENTIAL, CREDENTIAL_LIST


@responses.activate
def test_get_credentials(client):
    responses.add(responses.GET, f"{V1}/scv", json=CREDENTIAL_LIST)
    result = client.get_credentials()
    assert result["credential"][0]["alias"] == "my-device"


@responses.activate
def test_get_credential(client):
    responses.add(responses.GET, f"{V1}/scv/my-device", json=CREDENTIAL)
    result = client.get_credential("my-device")
    assert result["alias"] == "my-device"


@responses.activate
def test_create_credential(client):
    responses.add(responses.POST, f"{V1}/scv", status=201)
    data = {"alias": "new-device", "username": "admin", "password": "pass"}
    client.create_credential(data)
    body = json.loads(responses.calls[0].request.body)
    assert body["alias"] == "new-device"


@responses.activate
def test_update_credential(client):
    responses.add(responses.PUT, f"{V1}/scv/my-device", status=204)
    result = client.update_credential("my-device",
                                      {"username": "root", "password": "new"})
    assert result is None


@responses.activate
def test_delete_credential(client):
    responses.add(responses.DELETE, f"{V1}/scv/my-device", status=204)
    result = client.delete_credential("my-device")
    assert result is None
