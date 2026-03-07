"""Tests for EnLinkdMixin – /api/v2/enlinkd."""
import responses
from .conftest import V2
from .fixtures import (
    ENLINKD_DTO,
    LLDP_LINK_NODE,
    CDP_LINK_NODE,
    OSPF_LINK_NODE,
    ISIS_LINK_NODE,
    BRIDGE_LINK_NODE,
    LLDP_ELEMENT_NODE,
    CDP_ELEMENT_NODE,
    OSPF_ELEMENT_NODE,
    ISIS_ELEMENT_NODE,
    BRIDGE_ELEMENT_NODE,
)


@responses.activate
def test_get_node_enlinkd(client):
    responses.add(responses.GET, f"{V2}/enlinkd/1",
                  json=ENLINKD_DTO)
    result = client.get_node_enlinkd(1)
    assert result["lldpLinkNodes"][0]["lldpRemChassisId"] == "00:11:22:33:44:55"
    assert result["cdpElementNode"]["cdpGlobalDeviceId"] == "router01.example.com"


@responses.activate
def test_get_node_lldp_links(client):
    responses.add(responses.GET, f"{V2}/enlinkd/lldp_links/1",
                  json=[LLDP_LINK_NODE])
    result = client.get_node_lldp_links(1)
    assert result[0]["lldpLocalPort"] == "Gi0/0/0"
    assert result[0]["lldpRemPort"] == "Gi0/0/1"


@responses.activate
def test_get_node_cdp_links(client):
    responses.add(responses.GET, f"{V2}/enlinkd/cdp_links/1",
                  json=[CDP_LINK_NODE])
    result = client.get_node_cdp_links(1)
    assert result[0]["cdpCacheDevice"] == "router02.example.com"
    assert result[0]["cdpCachePlatform"] == "Cisco IOS Software, ISR4331"


@responses.activate
def test_get_node_ospf_links(client):
    responses.add(responses.GET, f"{V2}/enlinkd/ospf_links/1",
                  json=[OSPF_LINK_NODE])
    result = client.get_node_ospf_links(1)
    assert result[0]["ospfRemRouterId"] == "192.168.1.2"
    assert result[0]["ospfLinkInfo"] == "point-to-point"


@responses.activate
def test_get_node_isis_links(client):
    responses.add(responses.GET, f"{V2}/enlinkd/isis_links/1",
                  json=[ISIS_LINK_NODE])
    result = client.get_node_isis_links(1)
    assert result[0]["isisCircIfIndex"] == 6
    assert result[0]["isisISAdjState"] == "up"


@responses.activate
def test_get_node_bridge_links(client):
    responses.add(responses.GET, f"{V2}/enlinkd/bridge_links/1",
                  json=[BRIDGE_LINK_NODE])
    result = client.get_node_bridge_links(1)
    assert result[0]["bridgeLocalPort"] == "FastEthernet0/1"
    remotes = result[0]["BridgeLinkRemoteNodes"]
    assert remotes[0]["bridgeRemote"] == "switch02.example.com"


@responses.activate
def test_get_node_lldp_element(client):
    responses.add(responses.GET, f"{V2}/enlinkd/lldp_elems/1",
                  json=LLDP_ELEMENT_NODE)
    result = client.get_node_lldp_element(1)
    assert result["lldpChassisId"] == "00:11:22:33:44:55"
    assert result["lldpSysName"] == "router01"


@responses.activate
def test_get_node_cdp_element(client):
    responses.add(responses.GET, f"{V2}/enlinkd/cdp_elems/1",
                  json=CDP_ELEMENT_NODE)
    result = client.get_node_cdp_element(1)
    assert result["cdpGlobalDeviceId"] == "router01.example.com"
    assert result["cdpGlobalRun"] == "true"


@responses.activate
def test_get_node_ospf_element(client):
    responses.add(responses.GET, f"{V2}/enlinkd/ospf_elems/1",
                  json=OSPF_ELEMENT_NODE)
    result = client.get_node_ospf_element(1)
    assert result["ospfRouterId"] == "192.168.1.1"
    assert result["ospfVersionNumber"] == 2


@responses.activate
def test_get_node_isis_element(client):
    responses.add(responses.GET, f"{V2}/enlinkd/isis_elems/1",
                  json=ISIS_ELEMENT_NODE)
    result = client.get_node_isis_element(1)
    assert result["isisSysID"] == "0100.0200.0300"
    assert result["isisSysAdminState"] == "on"


@responses.activate
def test_get_node_bridge_elements(client):
    responses.add(responses.GET, f"{V2}/enlinkd/bridge_elems/1",
                  json=[BRIDGE_ELEMENT_NODE])
    result = client.get_node_bridge_elements(1)
    assert result[0]["baseBridgeAddress"] == "00:11:22:33:44:55"
    assert result[0]["baseNumPorts"] == 24
    assert result[0]["vlan"] == 1
