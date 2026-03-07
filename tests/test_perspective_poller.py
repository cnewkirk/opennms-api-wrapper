"""Tests for PerspectivePollerMixin – /api/v2/perspectivepoller."""
import responses
from .conftest import V2, qs
from .fixtures import PERSPECTIVE_POLLER_STATUS


@responses.activate
def test_get_perspective_poller_status(client):
    responses.add(responses.GET, f"{V2}/perspectivepoller/1",
                  json=PERSPECTIVE_POLLER_STATUS)
    result = client.get_perspective_poller_status(1)
    assert result["applicationId"] == 1


@responses.activate
def test_get_perspective_poller_status_with_time(client):
    responses.add(responses.GET, f"{V2}/perspectivepoller/1",
                  json=PERSPECTIVE_POLLER_STATUS)
    client.get_perspective_poller_status(1, start=1000, end=2000)
    params = qs(responses.calls[0].request.url)
    assert params["start"] == ["1000"]
    assert params["end"] == ["2000"]


@responses.activate
def test_get_perspective_poller_service_status(client):
    responses.add(responses.GET, f"{V2}/perspectivepoller/1/201",
                  json=PERSPECTIVE_POLLER_STATUS)
    result = client.get_perspective_poller_service_status(1, 201)
    assert result["applicationId"] == 1
