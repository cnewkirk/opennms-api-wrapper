"""Tests for LogsMixin – /rest/logs."""
import responses
from .conftest import V1, qs
from .fixtures import LOG_FILE_LIST, LOG_CONTENTS


@responses.activate
def test_get_log_files(client):
    responses.add(responses.GET, f"{V1}/logs", json=LOG_FILE_LIST)
    result = client.get_log_files()
    assert "manager.log" in result


@responses.activate
def test_get_log_contents(client):
    responses.add(responses.GET, f"{V1}/logs/contents",
                  json=LOG_CONTENTS)
    result = client.get_log_contents("manager.log", lines=100,
                                     reverse=False)
    assert "Manager started" in result[0]
    params = qs(responses.calls[0].request.url)
    assert params["f"] == ["manager.log"]
    assert params["n"] == ["100"]
    assert params["reverse"] == ["False"]


@responses.activate
def test_get_log_contents_missing_file(client):
    responses.add(responses.GET, f"{V1}/logs/contents", status=204)
    assert client.get_log_contents("nope.log") is None
