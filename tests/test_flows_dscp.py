"""Tests for FlowsMixin DSCP and flowGraphUrl methods."""
import responses
from .conftest import V1, qs
from .fixtures import (
    FLOW_DSCP, FLOW_DSCP_ENUMERATE, FLOW_DSCP_SERIES, FLOW_GRAPH_URL,
)


@responses.activate
def test_get_flow_dscp_defaults(client):
    responses.add(responses.GET, f"{V1}/flows/dscp", json=FLOW_DSCP)
    result = client.get_flow_dscp()
    assert result["headers"][0]["dscp"] == 0
    params = qs(responses.calls[0].request.url)
    assert params["N"] == ["10"]
    assert params["includeOther"] == ["false"]


@responses.activate
def test_get_flow_dscp_with_filters(client):
    responses.add(responses.GET, f"{V1}/flows/dscp", json=FLOW_DSCP)
    client.get_flow_dscp(top_n=5, if_index=6, exporter_node="1",
                         include_other=True)
    params = qs(responses.calls[0].request.url)
    assert params["N"] == ["5"]
    assert params["ifIndex"] == ["6"]
    assert params["exporterNode"] == ["1"]
    assert params["includeOther"] == ["true"]


@responses.activate
def test_get_flow_dscp_enumerate(client):
    responses.add(responses.GET, f"{V1}/flows/dscp/enumerate",
                  json=FLOW_DSCP_ENUMERATE)
    result = client.get_flow_dscp_enumerate()
    assert 0 in result["dscp"]
    assert qs(responses.calls[0].request.url)["limit"] == ["10"]


@responses.activate
def test_get_flow_dscp_series(client):
    responses.add(responses.GET, f"{V1}/flows/dscp/series",
                  json=FLOW_DSCP_SERIES)
    result = client.get_flow_dscp_series(top_n=3, step=60000)
    assert result["columns"][0]["label"] == "0"
    params = qs(responses.calls[0].request.url)
    assert params["N"] == ["3"]
    assert params["step"] == ["60000"]


@responses.activate
def test_get_flow_graph_url(client):
    responses.add(responses.GET, f"{V1}/flows/flowGraphUrl",
                  body="http://grafana:3000/d/flows",
                  content_type="text/plain")
    result = client.get_flow_graph_url()
    assert result == "http://grafana:3000/d/flows"
