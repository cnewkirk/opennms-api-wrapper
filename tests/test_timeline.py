"""Tests for TimelineMixin – /rest/timeline."""
import responses
from .conftest import V1
from .fixtures import TIMELINE_PNG, TIMELINE_HTML


@responses.activate
def test_get_timeline_header(client):
    responses.add(
        responses.GET,
        f"{V1}/timeline/header/1700000000/1700086400/500",
        body=TIMELINE_PNG, content_type="image/png")
    result = client.get_timeline_header(1700000000, 1700086400, 500)
    assert result == TIMELINE_PNG
    assert result.startswith(b"\x89PNG")


@responses.activate
def test_get_timeline_image(client):
    responses.add(
        responses.GET,
        f"{V1}/timeline/image/1/10.0.0.1/4/1700000000/1700086400/500",
        body=TIMELINE_PNG, content_type="image/png")
    result = client.get_timeline_image(1, "10.0.0.1", 4,
                                       1700000000, 1700086400, 500)
    assert result == TIMELINE_PNG


@responses.activate
def test_get_timeline_empty(client):
    responses.add(
        responses.GET,
        f"{V1}/timeline/empty/1700000000/1700086400/500",
        body=TIMELINE_PNG, content_type="image/png")
    result = client.get_timeline_empty(1700000000, 1700086400, 500)
    assert result == TIMELINE_PNG


@responses.activate
def test_get_timeline_html(client):
    responses.add(
        responses.GET,
        f"{V1}/timeline/html/1/10.0.0.1/4/1700000000/1700086400/500",
        body=TIMELINE_HTML, content_type="text/html")
    result = client.get_timeline_html(1, "10.0.0.1", 4,
                                      1700000000, 1700086400, 500)
    assert "<img" in result
