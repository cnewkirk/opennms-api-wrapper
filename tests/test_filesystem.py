"""Tests for FilesystemMixin – /rest/filesystem."""
import responses
from .conftest import V1, qs
from .fixtures import (
    FILESYSTEM_FILE_LIST, FILESYSTEM_EXTENSIONS, FILESYSTEM_HELP_MD,
    FILESYSTEM_CONTENTS_XML,
)


@responses.activate
def test_get_filesystem_files(client):
    responses.add(responses.GET, f"{V1}/filesystem",
                  json=FILESYSTEM_FILE_LIST)
    result = client.get_filesystem_files()
    assert "discovery-configuration.xml" in result
    assert "?" not in responses.calls[0].request.url


@responses.activate
def test_get_filesystem_files_changed_only(client):
    responses.add(responses.GET, f"{V1}/filesystem",
                  json=FILESYSTEM_FILE_LIST)
    client.get_filesystem_files(changed_only=True)
    params = qs(responses.calls[0].request.url)
    assert params["changedFilesOnly"] == ["true"]


@responses.activate
def test_get_filesystem_extensions(client):
    responses.add(responses.GET, f"{V1}/filesystem/extensions",
                  json=FILESYSTEM_EXTENSIONS)
    assert "xml" in client.get_filesystem_extensions()


@responses.activate
def test_get_filesystem_help(client):
    responses.add(responses.GET, f"{V1}/filesystem/help",
                  body=FILESYSTEM_HELP_MD,
                  content_type="text/markdown")
    result = client.get_filesystem_help("discovery-configuration.xml")
    assert result.startswith("# discovery-configuration.xml")
    params = qs(responses.calls[0].request.url)
    assert params["f"] == ["discovery-configuration.xml"]


@responses.activate
def test_get_filesystem_contents(client):
    responses.add(responses.GET, f"{V1}/filesystem/contents",
                  body=FILESYSTEM_CONTENTS_XML,
                  content_type="application/xml")
    result = client.get_filesystem_contents(
        "discovery-configuration.xml")
    assert "<discovery-configuration" in result


@responses.activate
def test_upload_filesystem_contents(client):
    responses.add(responses.POST, f"{V1}/filesystem/contents",
                  status=200)
    client.upload_filesystem_contents(
        "discovery-configuration.xml", FILESYSTEM_CONTENTS_XML)
    request = responses.calls[0].request
    assert qs(request.url)["f"] == ["discovery-configuration.xml"]
    assert request.headers["Content-Type"].startswith(
        "multipart/form-data")
    assert b"<discovery-configuration" in request.body


@responses.activate
def test_delete_filesystem_file(client):
    responses.add(responses.DELETE, f"{V1}/filesystem/contents",
                  status=200)
    assert client.delete_filesystem_file("obsolete.xml") is None
    params = qs(responses.calls[0].request.url)
    assert params["f"] == ["obsolete.xml"]
