"""Tests for RequisitionsMixin – /rest/requisitions."""
import json
import responses
from .conftest import V1, qs
from .fixtures import (
    REQUISITION, REQUISITION_LIST, REQUISITION_NODE, REQUISITION_NODE_LIST,
    REQUISITION_INTERFACE, REQUISITION_SERVICE,
    REQUISITION_CATEGORY, REQUISITION_ASSET,
)


@responses.activate
def test_get_requisitions(client):
    responses.add(responses.GET, f"{V1}/requisitions", json=REQUISITION_LIST)
    result = client.get_requisitions()
    assert result["requisition"][0]["foreign-source"] == "Routers"


@responses.activate
def test_get_requisition(client):
    responses.add(responses.GET, f"{V1}/requisitions/Routers", json=REQUISITION)
    result = client.get_requisition("Routers")
    assert result["foreign-source"] == "Routers"
    assert result["node-count"] == 1


@responses.activate
def test_get_requisition_count(client):
    responses.add(responses.GET, f"{V1}/requisitions/count",
                  body="3", content_type="text/plain")
    assert client.get_requisition_count() == 3


@responses.activate
def test_get_deployed_requisitions(client):
    responses.add(responses.GET, f"{V1}/requisitions/deployed",
                  json=REQUISITION_LIST)
    result = client.get_deployed_requisitions()
    assert result["requisition"][0]["foreign-source"] == "Routers"
    assert "/deployed" in responses.calls[0].request.url


@responses.activate
def test_get_deployed_requisition_count(client):
    responses.add(responses.GET, f"{V1}/requisitions/deployed/count",
                  body="2", content_type="text/plain")
    assert client.get_deployed_requisition_count() == 2


@responses.activate
def test_create_requisition(client):
    responses.add(responses.POST, f"{V1}/requisitions", json=REQUISITION, status=200)
    client.create_requisition({"foreign-source": "Routers", "node": []})
    body = json.loads(responses.calls[0].request.body)
    assert body["foreign-source"] == "Routers"
    assert responses.calls[0].request.headers["Content-Type"] == "application/json"


@responses.activate
def test_import_requisition(client):
    responses.add(responses.PUT, f"{V1}/requisitions/Routers/import", status=202)
    result = client.import_requisition("Routers")
    assert result is None
    assert "/Routers/import" in responses.calls[0].request.url
    assert "rescanExisting" not in responses.calls[0].request.url


@responses.activate
def test_import_requisition_no_rescan(client):
    responses.add(responses.PUT, f"{V1}/requisitions/Routers/import", status=202)
    client.import_requisition("Routers", rescan_existing=False)
    assert qs(responses.calls[0].request.url)["rescanExisting"] == ["false"]


@responses.activate
def test_update_requisition(client):
    responses.add(responses.PUT, f"{V1}/requisitions/Routers", status=204)
    client.update_requisition("Routers", {"date-stamp": "2024-06-01"})
    body = json.loads(responses.calls[0].request.body)
    assert "date-stamp" in body


@responses.activate
def test_delete_requisition(client):
    responses.add(responses.DELETE, f"{V1}/requisitions/Routers", status=202)
    result = client.delete_requisition("Routers")
    assert result is None


@responses.activate
def test_delete_deployed_requisition(client):
    responses.add(responses.DELETE, f"{V1}/requisitions/deployed/Routers",
                  status=202)
    result = client.delete_deployed_requisition("Routers")
    assert result is None
    assert "/deployed/Routers" in responses.calls[0].request.url


# ============================================================
# Nodes
# ============================================================

@responses.activate
def test_get_requisition_nodes(client):
    responses.add(responses.GET, f"{V1}/requisitions/Routers/nodes",
                  json=REQUISITION_NODE_LIST)
    result = client.get_requisition_nodes("Routers")
    assert result["node"][0]["foreign-id"] == "router01"


@responses.activate
def test_get_requisition_node(client):
    responses.add(responses.GET, f"{V1}/requisitions/Routers/nodes/router01",
                  json=REQUISITION_NODE)
    result = client.get_requisition_node("Routers", "router01")
    assert result["node-label"] == "router01.example.com"


@responses.activate
def test_create_requisition_node(client):
    responses.add(responses.POST, f"{V1}/requisitions/Routers/nodes",
                  json=REQUISITION_NODE, status=200)
    client.create_requisition_node("Routers", REQUISITION_NODE)
    body = json.loads(responses.calls[0].request.body)
    assert body["foreign-id"] == "router01"


@responses.activate
def test_update_requisition_node(client):
    responses.add(responses.PUT, f"{V1}/requisitions/Routers/nodes/router01",
                  status=204)
    client.update_requisition_node("Routers", "router01", {"node-label": "updated"})
    body = json.loads(responses.calls[0].request.body)
    assert body["node-label"] == "updated"


@responses.activate
def test_delete_requisition_node(client):
    responses.add(responses.DELETE, f"{V1}/requisitions/Routers/nodes/router01",
                  status=202)
    result = client.delete_requisition_node("Routers", "router01")
    assert result is None


# ============================================================
# Interfaces
# ============================================================

@responses.activate
def test_get_requisition_node_interfaces(client):
    responses.add(responses.GET,
                  f"{V1}/requisitions/Routers/nodes/router01/interfaces",
                  json={"interface": [REQUISITION_INTERFACE]})
    result = client.get_requisition_node_interfaces("Routers", "router01")
    assert result["interface"][0]["ip-addr"] == "192.168.1.1"


@responses.activate
def test_create_requisition_node_interface(client):
    responses.add(responses.POST,
                  f"{V1}/requisitions/Routers/nodes/router01/interfaces",
                  json=REQUISITION_INTERFACE, status=200)
    client.create_requisition_node_interface("Routers", "router01",
                                             REQUISITION_INTERFACE)
    body = json.loads(responses.calls[0].request.body)
    assert body["ip-addr"] == "192.168.1.1"


@responses.activate
def test_update_requisition_node_interface(client):
    responses.add(responses.PUT,
                  f"{V1}/requisitions/Routers/nodes/router01/interfaces/192.168.1.1",
                  status=204)
    client.update_requisition_node_interface("Routers", "router01",
                                             "192.168.1.1", {"snmp-primary": "S"})
    body = json.loads(responses.calls[0].request.body)
    assert body["snmp-primary"] == "S"


@responses.activate
def test_delete_requisition_node_interface(client):
    responses.add(responses.DELETE,
                  f"{V1}/requisitions/Routers/nodes/router01/interfaces/192.168.1.1",
                  status=202)
    result = client.delete_requisition_node_interface("Routers", "router01",
                                                       "192.168.1.1")
    assert result is None


# ============================================================
# Services
# ============================================================

@responses.activate
def test_get_requisition_node_services(client):
    responses.add(
        responses.GET,
        f"{V1}/requisitions/Routers/nodes/router01/interfaces/192.168.1.1/services",
        json={"monitored-service": [REQUISITION_SERVICE]})
    result = client.get_requisition_node_services("Routers", "router01",
                                                   "192.168.1.1")
    assert result["monitored-service"][0]["service-name"] == "ICMP"


@responses.activate
def test_create_requisition_node_service(client):
    responses.add(
        responses.POST,
        f"{V1}/requisitions/Routers/nodes/router01/interfaces/192.168.1.1/services",
        json=REQUISITION_SERVICE, status=200)
    client.create_requisition_node_service("Routers", "router01", "192.168.1.1",
                                           {"service-name": "HTTP"})
    body = json.loads(responses.calls[0].request.body)
    assert body["service-name"] == "HTTP"


@responses.activate
def test_delete_requisition_node_service(client):
    responses.add(
        responses.DELETE,
        f"{V1}/requisitions/Routers/nodes/router01/interfaces/192.168.1.1/services/ICMP",
        status=202)
    result = client.delete_requisition_node_service("Routers", "router01",
                                                     "192.168.1.1", "ICMP")
    assert result is None


# ============================================================
# Categories
# ============================================================

@responses.activate
def test_get_requisition_node_categories(client):
    responses.add(responses.GET,
                  f"{V1}/requisitions/Routers/nodes/router01/categories",
                  json={"category": [REQUISITION_CATEGORY]})
    result = client.get_requisition_node_categories("Routers", "router01")
    assert result["category"][0]["name"] == "Production"


@responses.activate
def test_add_requisition_node_category(client):
    responses.add(responses.POST,
                  f"{V1}/requisitions/Routers/nodes/router01/categories",
                  json=REQUISITION_CATEGORY, status=200)
    client.add_requisition_node_category("Routers", "router01",
                                         {"name": "Production"})
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "Production"


@responses.activate
def test_delete_requisition_node_category(client):
    responses.add(responses.DELETE,
                  f"{V1}/requisitions/Routers/nodes/router01/categories/Production",
                  status=202)
    result = client.delete_requisition_node_category("Routers", "router01",
                                                     "Production")
    assert result is None


# ============================================================
# Assets
# ============================================================

@responses.activate
def test_get_requisition_node_assets(client):
    responses.add(responses.GET,
                  f"{V1}/requisitions/Routers/nodes/router01/assets",
                  json={"asset": [REQUISITION_ASSET]})
    result = client.get_requisition_node_assets("Routers", "router01")
    assert result["asset"][0]["name"] == "manufacturer"


@responses.activate
def test_set_requisition_node_asset(client):
    responses.add(responses.POST,
                  f"{V1}/requisitions/Routers/nodes/router01/assets",
                  json=REQUISITION_ASSET, status=200)
    client.set_requisition_node_asset("Routers", "router01",
                                      {"name": "manufacturer", "value": "Cisco"})
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "manufacturer"
    assert body["value"] == "Cisco"


@responses.activate
def test_delete_requisition_node_asset(client):
    responses.add(responses.DELETE,
                  f"{V1}/requisitions/Routers/nodes/router01/assets/manufacturer",
                  status=202)
    result = client.delete_requisition_node_asset("Routers", "router01",
                                                  "manufacturer")
    assert result is None
