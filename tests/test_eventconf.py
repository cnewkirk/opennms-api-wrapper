"""Tests for EventConfMixin – /api/v2/eventconf."""
import json
import os
import tempfile
import responses
from .conftest import V2, qs
from .fixtures import (
    EVENTCONF_FILTER, EVENTCONF_SOURCES, EVENTCONF_SOURCE,
    EVENTCONF_SOURCE_NAMES, EVENTCONF_VENDOR_EVENTS, EVENTCONF_EVENT,
)


@responses.activate
def test_get_eventconf_filter(client):
    responses.add(responses.GET, f"{V2}/eventconf/filter",
                  json=EVENTCONF_FILTER)
    result = client.get_eventconf_filter(uei="nodeDown")
    assert result["events"][0]["uei"] == "uei.opennms.org/nodes/nodeDown"
    params = qs(responses.calls[0].request.url)
    assert params["uei"] == ["nodeDown"]


@responses.activate
def test_get_eventconf_filter_sources(client):
    responses.add(responses.GET, f"{V2}/eventconf/filter/sources",
                  json=EVENTCONF_SOURCES)
    result = client.get_eventconf_filter_sources()
    assert result["sources"][0]["id"] == "default"


@responses.activate
def test_get_eventconf_filter_events(client):
    responses.add(responses.GET, f"{V2}/eventconf/filter/default/events",
                  json=EVENTCONF_FILTER)
    result = client.get_eventconf_filter_events("default")
    assert len(result["events"]) >= 1


@responses.activate
def test_get_eventconf_source_names(client):
    responses.add(responses.GET, f"{V2}/eventconf/sources/names",
                  json=EVENTCONF_SOURCE_NAMES)
    result = client.get_eventconf_source_names()
    assert "default" in result


@responses.activate
def test_get_eventconf_source(client):
    responses.add(responses.GET, f"{V2}/eventconf/sources/default",
                  json=EVENTCONF_SOURCE)
    result = client.get_eventconf_source("default")
    assert result["id"] == "default"


@responses.activate
def test_download_eventconf_events(client):
    xml = "<events><event/></events>"
    responses.add(responses.GET,
                  f"{V2}/eventconf/sources/default/events/download",
                  body=xml, content_type="application/xml")
    result = client.download_eventconf_events("default")
    assert "<events>" in result


@responses.activate
def test_get_eventconf_vendor_events(client):
    responses.add(responses.GET, f"{V2}/eventconf/vendors/Cisco/events",
                  json=EVENTCONF_VENDOR_EVENTS)
    result = client.get_eventconf_vendor_events("Cisco")
    assert result["events"][0]["label"] == "BGP Up"


@responses.activate
def test_create_eventconf_event(client):
    responses.add(responses.POST,
                  f"{V2}/eventconf/sources/default/events",
                  json=EVENTCONF_EVENT, status=201)
    result = client.create_eventconf_event("default", EVENTCONF_EVENT)
    assert result["uei"] == "uei.opennms.org/custom/testEvent"


@responses.activate
def test_update_eventconf_event(client):
    responses.add(responses.PUT,
                  f"{V2}/eventconf/sources/default/events/evt-1",
                  status=204)
    result = client.update_eventconf_event("default", "evt-1",
                                           EVENTCONF_EVENT)
    assert result is None


@responses.activate
def test_set_eventconf_sources_status(client):
    responses.add(responses.PATCH, f"{V2}/eventconf/sources/status",
                  status=204)
    result = client.set_eventconf_sources_status({"default": True})
    assert result is None
    body = json.loads(responses.calls[0].request.body)
    assert body["default"] is True


@responses.activate
def test_set_eventconf_events_status(client):
    responses.add(responses.PATCH,
                  f"{V2}/eventconf/sources/default/events/status",
                  status=204)
    result = client.set_eventconf_events_status("default",
                                                {"evt-1": False})
    assert result is None


@responses.activate
def test_delete_eventconf_sources(client):
    responses.add(responses.DELETE, f"{V2}/eventconf/sources", status=204)
    result = client.delete_eventconf_sources({"ids": ["custom"]})
    assert result is None


@responses.activate
def test_delete_eventconf_events(client):
    responses.add(responses.DELETE,
                  f"{V2}/eventconf/sources/default/events", status=204)
    result = client.delete_eventconf_events("default",
                                            {"ids": ["evt-1"]})
    assert result is None


@responses.activate
def test_upload_eventconf_from_file(client):
    responses.add(responses.POST, f"{V2}/eventconf/upload", status=204)
    xml = b"<events><event-file>custom.xml</event-file></events>"
    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as fh:
        fh.write(xml)
        fh.flush()
        path = fh.name
    try:
        result = client.upload_eventconf(path)
    finally:
        os.unlink(path)
    assert result is None
    assert b"custom.xml" in responses.calls[0].request.body


@responses.activate
def test_upload_eventconf_from_bytes(client):
    responses.add(responses.POST, f"{V2}/eventconf/upload", status=204)
    xml = b"<events><event-file>custom.xml</event-file></events>"
    result = client.upload_eventconf(xml)
    assert result is None
    body = responses.calls[0].request.body
    assert b"custom.xml" in body
    assert b"events.xml" in body
