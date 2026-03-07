"""Tests for IpInterfacesV2Mixin – /api/v2/ipinterfaces (read-only)."""
import responses
from .conftest import V2, qs
from .fixtures import IP_INTERFACE_LIST


@responses.activate
def test_get_ip_interfaces_defaults(client):
    responses.add(responses.GET, f"{V2}/ipinterfaces",
                  json=IP_INTERFACE_LIST)
    result = client.get_ip_interfaces()
    assert result["ipInterface"][0]["ipAddress"] == "192.168.1.1"
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["10"]
    assert params["offset"] == ["0"]
    assert "_s" not in params


@responses.activate
def test_get_ip_interfaces_with_fiql(client):
    responses.add(responses.GET, f"{V2}/ipinterfaces",
                  json=IP_INTERFACE_LIST)
    result = client.get_ip_interfaces(fiql="ipAddress==192.168.1.1")
    assert result["ipInterface"][0]["nodeId"] == 1
    params = qs(responses.calls[0].request.url)
    assert params["_s"] == ["ipAddress==192.168.1.1"]


@responses.activate
def test_get_ip_interfaces_pagination(client):
    responses.add(responses.GET, f"{V2}/ipinterfaces",
                  json=IP_INTERFACE_LIST)
    client.get_ip_interfaces(limit=25, offset=50)
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["25"]
    assert params["offset"] == ["50"]


@responses.activate
def test_get_ip_interfaces_fiql_node_label(client):
    responses.add(responses.GET, f"{V2}/ipinterfaces",
                  json=IP_INTERFACE_LIST)
    client.get_ip_interfaces(fiql="node.label==router01.example.com")
    params = qs(responses.calls[0].request.url)
    assert params["_s"] == ["node.label==router01.example.com"]


@responses.activate
def test_get_ip_interfaces_uses_v2_url(client):
    responses.add(responses.GET, f"{V2}/ipinterfaces",
                  json=IP_INTERFACE_LIST)
    client.get_ip_interfaces()
    assert "/api/v2/ipinterfaces" in responses.calls[0].request.url
