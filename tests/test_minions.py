"""Tests for MinionsMixin – /rest/minions."""
import responses
from .conftest import V1
from .fixtures import MINION, MINION_LIST


@responses.activate
def test_get_minions(client):
    responses.add(responses.GET, f"{V1}/minions", json=MINION_LIST)
    result = client.get_minions()
    assert result["minion"][0]["id"] == "minion-01"


@responses.activate
def test_get_minion(client):
    responses.add(responses.GET, f"{V1}/minions/minion-01", json=MINION)
    result = client.get_minion("minion-01")
    assert result["id"] == "minion-01"
    assert result["location"] == "Default"


@responses.activate
def test_get_minion_count(client):
    responses.add(responses.GET, f"{V1}/minions/count",
                  body="2", content_type="text/plain")
    assert client.get_minion_count() == 2
