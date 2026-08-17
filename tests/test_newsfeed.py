"""Tests for NewsFeedMixin – /api/v2/newsfeed."""
import responses
from .conftest import V2
from .fixtures import NEWSFEED


@responses.activate
def test_get_newsfeed(client):
    responses.add(responses.GET, f"{V2}/newsfeed", json=NEWSFEED)
    result = client.get_newsfeed()
    assert result["items"][0]["categories"] == ["Releases"]
