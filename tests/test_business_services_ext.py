"""Tests for BusinessServicesMixin extended methods – edges, functions, reload."""
import json
import responses
from .conftest import V2
from .fixtures import (
    BS_EDGE, BS_MAP_FUNCTION, BS_MAP_FUNCTIONS,
    BS_REDUCE_FUNCTION, BS_REDUCE_FUNCTIONS, BUSINESS_SERVICE,
)


@responses.activate
def test_get_business_service_edge(client):
    responses.add(responses.GET, f"{V2}/business-services/edges/2001",
                  json=BS_EDGE)
    result = client.get_business_service_edge(2001)
    assert result["id"] == 2001
    assert result["type"] == "IP_SERVICE"


@responses.activate
def test_add_ip_service_edge(client):
    responses.add(responses.POST,
                  f"{V2}/business-services/1001/ip-service-edge",
                  json=BS_EDGE, status=201)
    edge = {"ipServiceId": 201, "mapFunction": {"type": "Identity"}, "weight": 1}
    result = client.add_ip_service_edge(1001, edge)
    assert result["id"] == 2001
    body = json.loads(responses.calls[0].request.body)
    assert body["ipServiceId"] == 201


@responses.activate
def test_add_reduction_key_edge(client):
    responses.add(responses.POST,
                  f"{V2}/business-services/1001/reduction-key-edge",
                  json=BS_EDGE, status=201)
    edge = {"reductionKey": "uei/test::1", "mapFunction": {"type": "Identity"}, "weight": 1}
    client.add_reduction_key_edge(1001, edge)
    body = json.loads(responses.calls[0].request.body)
    assert body["reductionKey"] == "uei/test::1"


@responses.activate
def test_add_child_edge(client):
    responses.add(responses.POST,
                  f"{V2}/business-services/1001/child-edge",
                  json=BS_EDGE, status=201)
    edge = {"childId": 1002, "mapFunction": {"type": "Identity"}, "weight": 1}
    client.add_child_edge(1001, edge)
    body = json.loads(responses.calls[0].request.body)
    assert body["childId"] == 1002


@responses.activate
def test_remove_business_service_edge(client):
    responses.add(responses.DELETE,
                  f"{V2}/business-services/1001/edges/2001",
                  status=204)
    result = client.remove_business_service_edge(1001, 2001)
    assert result is None


@responses.activate
def test_reload_business_service_daemon(client):
    responses.add(responses.POST,
                  f"{V2}/business-services/daemon/reload",
                  status=204)
    result = client.reload_business_service_daemon()
    assert result is None


@responses.activate
def test_get_map_functions(client):
    responses.add(responses.GET,
                  f"{V2}/business-services/functions/map",
                  json=BS_MAP_FUNCTIONS)
    result = client.get_map_functions()
    assert result[0]["name"] == "Identity"


@responses.activate
def test_get_map_function(client):
    responses.add(responses.GET,
                  f"{V2}/business-services/functions/map/Identity",
                  json=BS_MAP_FUNCTION)
    result = client.get_map_function("Identity")
    assert result["type"] == "Identity"


@responses.activate
def test_get_reduce_functions(client):
    responses.add(responses.GET,
                  f"{V2}/business-services/functions/reduce",
                  json=BS_REDUCE_FUNCTIONS)
    result = client.get_reduce_functions()
    assert result[0]["name"] == "HighestSeverity"


@responses.activate
def test_get_reduce_function(client):
    responses.add(responses.GET,
                  f"{V2}/business-services/functions/reduce/HighestSeverity",
                  json=BS_REDUCE_FUNCTION)
    result = client.get_reduce_function("HighestSeverity")
    assert result["type"] == "HighestSeverity"
