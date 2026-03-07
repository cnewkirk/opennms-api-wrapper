"""Tests for ApplicationsMixin – /api/v2/applications."""
import json
import responses
from .conftest import V2, qs
from .fixtures import APPLICATION, APPLICATION_LIST


@responses.activate
def test_get_applications(client):
    responses.add(responses.GET, f"{V2}/applications",
                  json=APPLICATION_LIST)
    result = client.get_applications()
    assert result["application"][0]["name"] == "Web Services"


@responses.activate
def test_get_application(client):
    responses.add(responses.GET, f"{V2}/applications/1",
                  json=APPLICATION)
    result = client.get_application(1)
    assert result["id"] == 1


@responses.activate
def test_create_application(client):
    responses.add(responses.POST, f"{V2}/applications",
                  json=APPLICATION, status=201)
    app = {"name": "Web Services"}
    result = client.create_application(app)
    assert result["id"] == 1
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "Web Services"


@responses.activate
def test_delete_application(client):
    responses.add(responses.DELETE, f"{V2}/applications/1", status=204)
    result = client.delete_application(1)
    assert result is None
