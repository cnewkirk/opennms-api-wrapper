"""Tests for MetadataMixin – /api/v2/nodes/{id}/metadata and sub-resources."""
import json
import responses
from .conftest import V2
from .fixtures import METADATA_LIST, METADATA_ENTRY

NODE_ID = 1
IP = "192.168.1.1"
SVC = "ICMP"
CTX = "X-OpenNMS-System"
KEY = "managedBy"
VAL = "ansible-tower"

# Base paths for convenience
_NODE = f"{V2}/nodes/{NODE_ID}/metadata"
_IFACE = f"{V2}/nodes/{NODE_ID}/ipinterfaces/{IP}/metadata"
_SVC = f"{V2}/nodes/{NODE_ID}/ipinterfaces/{IP}/services/{SVC}/metadata"


# ===========================================================================
# Node metadata
# ===========================================================================

@responses.activate
def test_get_node_metadata(client):
    responses.add(responses.GET, _NODE, json=METADATA_LIST)
    result = client.get_node_metadata(NODE_ID)
    assert result[0]["context"] == CTX
    assert result[0]["key"] == KEY
    assert f"/nodes/{NODE_ID}/metadata" in responses.calls[0].request.url


@responses.activate
def test_get_node_metadata_context(client):
    responses.add(responses.GET, f"{_NODE}/{CTX}", json=METADATA_LIST)
    result = client.get_node_metadata_context(NODE_ID, CTX)
    assert isinstance(result, list)
    assert f"/metadata/{CTX}" in responses.calls[0].request.url


@responses.activate
def test_get_node_metadata_value(client):
    responses.add(responses.GET, f"{_NODE}/{CTX}/{KEY}",
                  json=METADATA_ENTRY)
    result = client.get_node_metadata_value(NODE_ID, CTX, KEY)
    assert result["value"] == VAL
    assert f"/metadata/{CTX}/{KEY}" in responses.calls[0].request.url


@responses.activate
def test_set_node_metadata(client):
    responses.add(responses.POST, _NODE, status=204)
    payload = [{"context": CTX, "key": KEY, "value": VAL}]
    result = client.set_node_metadata(NODE_ID, payload)
    assert result is None
    body = json.loads(responses.calls[0].request.body)
    assert body[0]["context"] == CTX
    assert body[0]["value"] == VAL


@responses.activate
def test_set_node_metadata_value(client):
    responses.add(responses.PUT, f"{_NODE}/{CTX}/{KEY}/{VAL}",
                  status=204)
    result = client.set_node_metadata_value(NODE_ID, CTX, KEY, VAL)
    assert result is None
    assert (f"/metadata/{CTX}/{KEY}/{VAL}"
            in responses.calls[0].request.url)


@responses.activate
def test_delete_node_metadata_context(client):
    responses.add(responses.DELETE, f"{_NODE}/{CTX}", status=204)
    result = client.delete_node_metadata_context(NODE_ID, CTX)
    assert result is None
    assert responses.calls[0].request.method == "DELETE"
    assert f"/metadata/{CTX}" in responses.calls[0].request.url


@responses.activate
def test_delete_node_metadata_key(client):
    responses.add(responses.DELETE, f"{_NODE}/{CTX}/{KEY}",
                  status=204)
    result = client.delete_node_metadata_key(NODE_ID, CTX, KEY)
    assert result is None
    assert f"/metadata/{CTX}/{KEY}" in responses.calls[0].request.url


# ===========================================================================
# Interface metadata
# ===========================================================================

@responses.activate
def test_get_interface_metadata(client):
    responses.add(responses.GET, _IFACE, json=METADATA_LIST)
    result = client.get_interface_metadata(NODE_ID, IP)
    assert isinstance(result, list)
    assert f"/ipinterfaces/{IP}/metadata" in responses.calls[0].request.url


@responses.activate
def test_get_interface_metadata_context(client):
    responses.add(responses.GET, f"{_IFACE}/{CTX}", json=METADATA_LIST)
    result = client.get_interface_metadata_context(NODE_ID, IP, CTX)
    assert isinstance(result, list)
    assert f"/metadata/{CTX}" in responses.calls[0].request.url


@responses.activate
def test_get_interface_metadata_value(client):
    responses.add(responses.GET, f"{_IFACE}/{CTX}/{KEY}",
                  json=METADATA_ENTRY)
    result = client.get_interface_metadata_value(NODE_ID, IP, CTX, KEY)
    assert result["key"] == KEY
    assert f"/metadata/{CTX}/{KEY}" in responses.calls[0].request.url


@responses.activate
def test_set_interface_metadata(client):
    responses.add(responses.POST, _IFACE, status=204)
    payload = [{"context": CTX, "key": KEY, "value": VAL}]
    result = client.set_interface_metadata(NODE_ID, IP, payload)
    assert result is None
    body = json.loads(responses.calls[0].request.body)
    assert body[0]["key"] == KEY


@responses.activate
def test_set_interface_metadata_value(client):
    responses.add(responses.PUT, f"{_IFACE}/{CTX}/{KEY}/{VAL}",
                  status=204)
    result = client.set_interface_metadata_value(
        NODE_ID, IP, CTX, KEY, VAL)
    assert result is None
    assert (f"/metadata/{CTX}/{KEY}/{VAL}"
            in responses.calls[0].request.url)


@responses.activate
def test_delete_interface_metadata_context(client):
    responses.add(responses.DELETE, f"{_IFACE}/{CTX}", status=204)
    result = client.delete_interface_metadata_context(NODE_ID, IP, CTX)
    assert result is None
    assert responses.calls[0].request.method == "DELETE"


@responses.activate
def test_delete_interface_metadata_key(client):
    responses.add(responses.DELETE, f"{_IFACE}/{CTX}/{KEY}",
                  status=204)
    result = client.delete_interface_metadata_key(NODE_ID, IP, CTX, KEY)
    assert result is None
    assert f"/metadata/{CTX}/{KEY}" in responses.calls[0].request.url


# ===========================================================================
# Service metadata
# ===========================================================================

@responses.activate
def test_get_service_metadata(client):
    responses.add(responses.GET, _SVC, json=METADATA_LIST)
    result = client.get_service_metadata(NODE_ID, IP, SVC)
    assert isinstance(result, list)
    assert f"/services/{SVC}/metadata" in responses.calls[0].request.url


@responses.activate
def test_get_service_metadata_context(client):
    responses.add(responses.GET, f"{_SVC}/{CTX}", json=METADATA_LIST)
    result = client.get_service_metadata_context(NODE_ID, IP, SVC, CTX)
    assert isinstance(result, list)
    assert f"/metadata/{CTX}" in responses.calls[0].request.url


@responses.activate
def test_get_service_metadata_value(client):
    responses.add(responses.GET, f"{_SVC}/{CTX}/{KEY}",
                  json=METADATA_ENTRY)
    result = client.get_service_metadata_value(
        NODE_ID, IP, SVC, CTX, KEY)
    assert result["value"] == VAL
    assert f"/metadata/{CTX}/{KEY}" in responses.calls[0].request.url


@responses.activate
def test_set_service_metadata(client):
    responses.add(responses.POST, _SVC, status=204)
    payload = [{"context": CTX, "key": KEY, "value": VAL}]
    result = client.set_service_metadata(NODE_ID, IP, SVC, payload)
    assert result is None
    body = json.loads(responses.calls[0].request.body)
    assert body[0]["value"] == VAL


@responses.activate
def test_set_service_metadata_value(client):
    responses.add(responses.PUT, f"{_SVC}/{CTX}/{KEY}/{VAL}",
                  status=204)
    result = client.set_service_metadata_value(
        NODE_ID, IP, SVC, CTX, KEY, VAL)
    assert result is None
    assert (f"/metadata/{CTX}/{KEY}/{VAL}"
            in responses.calls[0].request.url)


@responses.activate
def test_delete_service_metadata_context(client):
    responses.add(responses.DELETE, f"{_SVC}/{CTX}", status=204)
    result = client.delete_service_metadata_context(
        NODE_ID, IP, SVC, CTX)
    assert result is None
    assert responses.calls[0].request.method == "DELETE"


@responses.activate
def test_delete_service_metadata_key(client):
    responses.add(responses.DELETE, f"{_SVC}/{CTX}/{KEY}",
                  status=204)
    result = client.delete_service_metadata_key(
        NODE_ID, IP, SVC, CTX, KEY)
    assert result is None
    assert f"/metadata/{CTX}/{KEY}" in responses.calls[0].request.url
