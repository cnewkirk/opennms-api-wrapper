"""Tests for UserDefinedLinksMixin – /api/v2/userdefinedlinks."""
import json
import responses
from .conftest import V2
from .fixtures import USER_DEFINED_LINK, USER_DEFINED_LINK_LIST


@responses.activate
def test_get_user_defined_links(client):
    responses.add(responses.GET, f"{V2}/userdefinedlinks",
                  json=USER_DEFINED_LINK_LIST)
    result = client.get_user_defined_links()
    assert result["user-defined-link"][0]["linkLabel"] == "Cross connect"


@responses.activate
def test_get_user_defined_link(client):
    responses.add(responses.GET, f"{V2}/userdefinedlinks/1",
                  json=USER_DEFINED_LINK)
    result = client.get_user_defined_link(1)
    assert result["id"] == 1


@responses.activate
def test_create_user_defined_link(client):
    responses.add(responses.POST, f"{V2}/userdefinedlinks",
                  json=USER_DEFINED_LINK, status=201)
    link = {"nodeIdA": 1, "nodeIdZ": 2, "linkLabel": "Cross connect"}
    result = client.create_user_defined_link(link)
    assert result["id"] == 1
    body = json.loads(responses.calls[0].request.body)
    assert body["nodeIdA"] == 1


@responses.activate
def test_delete_user_defined_link(client):
    responses.add(responses.DELETE, f"{V2}/userdefinedlinks/1",
                  status=204)
    result = client.delete_user_defined_link(1)
    assert result is None
