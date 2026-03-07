"""Tests for NodesMixin – /rest/nodes and sub-resources."""
import json
import responses
from .conftest import V1, V2, qs
from .fixtures import (
    NODE, NODE_LIST,
    IP_INTERFACE, IP_INTERFACE_LIST,
    SNMP_INTERFACE, SNMP_INTERFACE_LIST,
    MONITORED_SERVICE, MONITORED_SERVICE_LIST,
    ASSET_RECORD, HARDWARE_ENTITY,
    CATEGORY,
)

NEW_NODE = {"label": "newnode.example.com", "type": "A", "foreignSource": "Test",
            "foreignId": "newnode01", "location": "Default"}

NEW_IFACE = {"ipAddress": "10.0.0.1", "snmpPrimary": "P", "isManaged": "M"}
NEW_SNMP = {"ifIndex": 1, "ifName": "lo", "ifType": 24, "collect": "C"}
NEW_SERVICE = {"serviceType": {"name": "HTTP"}}
NEW_CATEGORY = {"name": "Production"}
NEW_ASSET = {"manufacturer": "Cisco", "modelNumber": "ISR4331"}


# ============================================================
# Nodes
# ============================================================

@responses.activate
def test_get_nodes_default(client):
    responses.add(responses.GET, f"{V1}/nodes", json=NODE_LIST)
    result = client.get_nodes()
    assert result["node"][0]["id"] == 1
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["10"]
    assert params["offset"] == ["0"]


@responses.activate
def test_get_nodes_with_filters(client):
    responses.add(responses.GET, f"{V1}/nodes", json=NODE_LIST)
    client.get_nodes(limit=100, foreignSource="Routers", order_by="label")
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["100"]
    assert params["foreignSource"] == ["Routers"]
    assert params["orderBy"] == ["label"]


@responses.activate
def test_get_node(client):
    responses.add(responses.GET, f"{V1}/nodes/1", json=NODE)
    result = client.get_node(1)
    assert result["id"] == 1
    assert result["label"] == "router01.example.com"


@responses.activate
def test_get_node_by_fs_fid(client):
    responses.add(responses.GET, f"{V1}/nodes/Routers:router01", json=NODE)
    result = client.get_node("Routers:router01")
    assert result["foreignSource"] == "Routers"


@responses.activate
def test_get_node_count(client):
    responses.add(responses.GET, f"{V2}/nodes",
                  json={"totalCount": 57, "count": 1, "offset": 0, "node": []})
    result = client.get_node_count()
    assert result == 57
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["1"]


@responses.activate
def test_create_node(client):
    responses.add(responses.POST, f"{V1}/nodes", json=NODE, status=201)
    result = client.create_node(NEW_NODE)
    assert result["id"] == 1
    body = json.loads(responses.calls[0].request.body)
    assert body["label"] == "newnode.example.com"
    assert body["foreignSource"] == "Test"
    assert responses.calls[0].request.headers["Content-Type"] == "application/json"


@responses.activate
def test_update_node(client):
    responses.add(responses.PUT, f"{V1}/nodes/1", status=204)
    result = client.update_node(1, {"label": "updated-label"})
    assert result is None
    body = json.loads(responses.calls[0].request.body)
    assert body["label"] == "updated-label"


@responses.activate
def test_delete_node(client):
    responses.add(responses.DELETE, f"{V1}/nodes/1", status=202)
    result = client.delete_node(1)
    assert result is None


@responses.activate
def test_rescan_node(client):
    responses.add(responses.POST, f"{V1}/nodes/1/rescan", status=204)
    result = client.rescan_node(1)
    assert result is None


# ============================================================
# IP Interfaces
# ============================================================

@responses.activate
def test_get_node_ip_interfaces(client):
    responses.add(responses.GET, f"{V1}/nodes/1/ipinterfaces",
                  json=IP_INTERFACE_LIST)
    result = client.get_node_ip_interfaces(1)
    assert result["ipInterface"][0]["ipAddress"] == "192.168.1.1"
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["10"]
    assert params["offset"] == ["0"]


@responses.activate
def test_get_node_ip_interface(client):
    responses.add(responses.GET, f"{V1}/nodes/1/ipinterfaces/192.168.1.1",
                  json=IP_INTERFACE)
    result = client.get_node_ip_interface(1, "192.168.1.1")
    assert result["ipAddress"] == "192.168.1.1"
    assert result["snmpPrimary"] == "P"


@responses.activate
def test_create_node_ip_interface(client):
    responses.add(responses.POST, f"{V1}/nodes/1/ipinterfaces",
                  json=IP_INTERFACE, status=201)
    result = client.create_node_ip_interface(1, NEW_IFACE)
    assert result["ipAddress"] == "192.168.1.1"
    body = json.loads(responses.calls[0].request.body)
    assert body["ipAddress"] == "10.0.0.1"
    assert body["snmpPrimary"] == "P"


@responses.activate
def test_update_node_ip_interface(client):
    responses.add(responses.PUT, f"{V1}/nodes/1/ipinterfaces/192.168.1.1",
                  status=204)
    client.update_node_ip_interface(1, "192.168.1.1", {"isManaged": "U"})
    body = json.loads(responses.calls[0].request.body)
    assert body["isManaged"] == "U"


@responses.activate
def test_delete_node_ip_interface(client):
    responses.add(responses.DELETE, f"{V1}/nodes/1/ipinterfaces/192.168.1.1",
                  status=202)
    result = client.delete_node_ip_interface(1, "192.168.1.1")
    assert result is None


# ============================================================
# Monitored Services
# ============================================================

@responses.activate
def test_get_node_ip_services(client):
    responses.add(responses.GET,
                  f"{V1}/nodes/1/ipinterfaces/192.168.1.1/services",
                  json=MONITORED_SERVICE_LIST)
    result = client.get_node_ip_services(1, "192.168.1.1")
    assert result["service"][0]["serviceName"] == "ICMP"


@responses.activate
def test_get_node_ip_service(client):
    responses.add(responses.GET,
                  f"{V1}/nodes/1/ipinterfaces/192.168.1.1/services/ICMP",
                  json=MONITORED_SERVICE)
    result = client.get_node_ip_service(1, "192.168.1.1", "ICMP")
    assert result["serviceName"] == "ICMP"
    assert result["status"] == "A"


@responses.activate
def test_create_node_ip_service(client):
    responses.add(responses.POST,
                  f"{V1}/nodes/1/ipinterfaces/192.168.1.1/services",
                  json=MONITORED_SERVICE, status=201)
    result = client.create_node_ip_service(1, "192.168.1.1", NEW_SERVICE)
    body = json.loads(responses.calls[0].request.body)
    assert body["serviceType"]["name"] == "HTTP"


@responses.activate
def test_delete_node_ip_service(client):
    responses.add(responses.DELETE,
                  f"{V1}/nodes/1/ipinterfaces/192.168.1.1/services/ICMP",
                  status=202)
    result = client.delete_node_ip_service(1, "192.168.1.1", "ICMP")
    assert result is None


# ============================================================
# SNMP Interfaces
# ============================================================

@responses.activate
def test_get_node_snmp_interfaces(client):
    responses.add(responses.GET, f"{V1}/nodes/1/snmpinterfaces",
                  json=SNMP_INTERFACE_LIST)
    result = client.get_node_snmp_interfaces(1)
    assert result["snmpInterface"][0]["ifIndex"] == 6


@responses.activate
def test_get_node_snmp_interface(client):
    responses.add(responses.GET, f"{V1}/nodes/1/snmpinterfaces/6",
                  json=SNMP_INTERFACE)
    result = client.get_node_snmp_interface(1, 6)
    assert result["ifIndex"] == 6
    assert result["ifOperStatus"] == 1


@responses.activate
def test_create_node_snmp_interface(client):
    responses.add(responses.POST, f"{V1}/nodes/1/snmpinterfaces",
                  json=SNMP_INTERFACE, status=201)
    client.create_node_snmp_interface(1, NEW_SNMP)
    body = json.loads(responses.calls[0].request.body)
    assert body["ifIndex"] == 1


@responses.activate
def test_update_node_snmp_interface(client):
    responses.add(responses.PUT, f"{V1}/nodes/1/snmpinterfaces/6", status=204)
    client.update_node_snmp_interface(1, 6, {"ifAlias": "new-alias"})
    body = json.loads(responses.calls[0].request.body)
    assert body["ifAlias"] == "new-alias"


@responses.activate
def test_delete_node_snmp_interface(client):
    responses.add(responses.DELETE, f"{V1}/nodes/1/snmpinterfaces/6", status=204)
    result = client.delete_node_snmp_interface(1, 6)
    assert result is None


# ============================================================
# Categories
# ============================================================

@responses.activate
def test_get_node_categories(client):
    responses.add(responses.GET, f"{V1}/nodes/1/categories",
                  json={"category": [CATEGORY]})
    result = client.get_node_categories(1)
    assert result["category"][0]["name"] == "Production"


@responses.activate
def test_get_node_category(client):
    responses.add(responses.GET, f"{V1}/nodes/1/categories/Production",
                  json=CATEGORY)
    result = client.get_node_category(1, "Production")
    assert result["name"] == "Production"


@responses.activate
def test_add_node_category(client):
    responses.add(responses.POST, f"{V1}/nodes/1/categories",
                  json=CATEGORY, status=201)
    client.add_node_category(1, NEW_CATEGORY)
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "Production"


@responses.activate
def test_update_node_category(client):
    responses.add(responses.PUT, f"{V1}/nodes/1/categories/Production",
                  status=204)
    client.update_node_category(1, "Production", {"name": "Production"})
    assert responses.calls[0].request.method == "PUT"


@responses.activate
def test_delete_node_category(client):
    responses.add(responses.DELETE, f"{V1}/nodes/1/categories/Production",
                  status=204)
    result = client.delete_node_category(1, "Production")
    assert result is None


# ============================================================
# Asset Record
# ============================================================

@responses.activate
def test_get_node_asset_record(client):
    responses.add(responses.GET, f"{V1}/nodes/1/assetRecord", json=ASSET_RECORD)
    result = client.get_node_asset_record(1)
    assert result["manufacturer"] == "Cisco"
    assert result["serialNumber"] == "FDO2147A0BC"


@responses.activate
def test_update_node_asset_record(client):
    responses.add(responses.PUT, f"{V1}/nodes/1/assetRecord", status=204)
    client.update_node_asset_record(1, NEW_ASSET)
    body = json.loads(responses.calls[0].request.body)
    assert body["manufacturer"] == "Cisco"
    assert body["modelNumber"] == "ISR4331"


# ============================================================
# Hardware Inventory
# ============================================================

@responses.activate
def test_get_node_hardware_inventory(client):
    responses.add(responses.GET, f"{V1}/nodes/1/hardwareInventory",
                  json=HARDWARE_ENTITY)
    result = client.get_node_hardware_inventory(1)
    assert result["entPhysicalMfgName"] == "Cisco Systems"
    assert result["entityPhysicalIndex"] == 1


@responses.activate
def test_get_node_hardware_entity(client):
    responses.add(responses.GET, f"{V1}/nodes/1/hardwareInventory/1",
                  json=HARDWARE_ENTITY)
    result = client.get_node_hardware_entity(1, 1)
    assert result["entPhysicalModelName"] == "ISR4331"


@responses.activate
def test_add_node_hardware_inventory(client):
    responses.add(responses.POST, f"{V1}/nodes/1/hardwareInventory",
                  json=HARDWARE_ENTITY, status=201)
    client.add_node_hardware_inventory(1, HARDWARE_ENTITY)
    body = json.loads(responses.calls[0].request.body)
    assert body["entityPhysicalIndex"] == 1


@responses.activate
def test_update_node_hardware_entity(client):
    responses.add(responses.PUT, f"{V1}/nodes/1/hardwareInventory/1", status=204)
    client.update_node_hardware_entity(1, 1, {"entPhysicalAlias": "chassis"})
    body = json.loads(responses.calls[0].request.body)
    assert body["entPhysicalAlias"] == "chassis"


@responses.activate
def test_delete_node_hardware_entity(client):
    responses.add(responses.DELETE, f"{V1}/nodes/1/hardwareInventory/1",
                  status=204)
    result = client.delete_node_hardware_entity(1, 1)
    assert result is None
