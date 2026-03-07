"""Tests for FlowsMixin – /rest/flows."""
import responses
from .conftest import V1, qs
from .fixtures import (
    FLOW_EXPORTER, FLOW_EXPORTER_LIST,
    FLOW_APPLICATIONS, FLOW_APPLICATIONS_ENUMERATE, FLOW_SERIES,
    FLOW_CONVERSATIONS, FLOW_HOSTS,
)


@responses.activate
def test_get_flow_count(client):
    responses.add(responses.GET, f"{V1}/flows/count",
                  body="1048576", content_type="text/plain")
    assert client.get_flow_count() == 1048576


@responses.activate
def test_get_flow_exporters(client):
    responses.add(responses.GET, f"{V1}/flows/exporters",
                  json=FLOW_EXPORTER_LIST)
    result = client.get_flow_exporters()
    assert result["exporters"][0]["node"]["id"] == 1


@responses.activate
def test_get_flow_exporter(client):
    responses.add(responses.GET, f"{V1}/flows/exporters/1",
                  json=FLOW_EXPORTER)
    result = client.get_flow_exporter("1")
    assert result["node"]["foreignSource"] == "Routers"


# ============================================================
# Applications
# ============================================================

@responses.activate
def test_get_flow_applications_defaults(client):
    responses.add(responses.GET, f"{V1}/flows/applications",
                  json=FLOW_APPLICATIONS)
    result = client.get_flow_applications()
    assert result["applications"][0]["application"] == "HTTP"
    params = qs(responses.calls[0].request.url)
    assert params["N"] == ["10"]
    assert params["start"] == ["-14400000"]
    assert params["end"] == ["0"]
    assert params["includeOther"] == ["false"]


@responses.activate
def test_get_flow_applications_with_filters(client):
    responses.add(responses.GET, f"{V1}/flows/applications",
                  json=FLOW_APPLICATIONS)
    client.get_flow_applications(top_n=5, if_index=6, exporter_node="1",
                                 include_other=True)
    params = qs(responses.calls[0].request.url)
    assert params["N"] == ["5"]
    assert params["ifIndex"] == ["6"]
    assert params["exporterNode"] == ["1"]
    assert params["includeOther"] == ["true"]


@responses.activate
def test_get_flow_applications_enumerate(client):
    responses.add(responses.GET, f"{V1}/flows/applications/enumerate",
                  json=FLOW_APPLICATIONS_ENUMERATE)
    result = client.get_flow_applications_enumerate()
    assert "HTTP" in result["label"]
    assert qs(responses.calls[0].request.url)["limit"] == ["10"]


@responses.activate
def test_get_flow_applications_series(client):
    responses.add(responses.GET, f"{V1}/flows/applications/series",
                  json=FLOW_SERIES)
    result = client.get_flow_applications_series(top_n=3, step=60000)
    assert result["columns"][0]["label"] == "HTTP"
    params = qs(responses.calls[0].request.url)
    assert params["N"] == ["3"]
    assert params["step"] == ["60000"]


# ============================================================
# Conversations
# ============================================================

@responses.activate
def test_get_flow_conversations_defaults(client):
    responses.add(responses.GET, f"{V1}/flows/conversations",
                  json=FLOW_CONVERSATIONS)
    result = client.get_flow_conversations()
    assert result["conversations"][0]["protocol"] == "TCP"
    assert qs(responses.calls[0].request.url)["N"] == ["10"]


@responses.activate
def test_get_flow_conversations_enumerate(client):
    responses.add(responses.GET, f"{V1}/flows/conversations/enumerate",
                  json={"conversation": []})
    client.get_flow_conversations_enumerate(limit=20)
    assert qs(responses.calls[0].request.url)["limit"] == ["20"]


@responses.activate
def test_get_flow_conversations_series(client):
    responses.add(responses.GET, f"{V1}/flows/conversations/series",
                  json=FLOW_SERIES)
    client.get_flow_conversations_series(top_n=5)
    assert qs(responses.calls[0].request.url)["N"] == ["5"]


# ============================================================
# Hosts
# ============================================================

@responses.activate
def test_get_flow_hosts_defaults(client):
    responses.add(responses.GET, f"{V1}/flows/hosts", json=FLOW_HOSTS)
    result = client.get_flow_hosts()
    assert result["hosts"][0]["host"] == "192.168.1.1"
    assert qs(responses.calls[0].request.url)["N"] == ["10"]


@responses.activate
def test_get_flow_hosts_enumerate(client):
    responses.add(responses.GET, f"{V1}/flows/hosts/enumerate",
                  json={"host": []})
    client.get_flow_hosts_enumerate(limit=25)
    assert qs(responses.calls[0].request.url)["limit"] == ["25"]


@responses.activate
def test_get_flow_hosts_series(client):
    responses.add(responses.GET, f"{V1}/flows/hosts/series", json=FLOW_SERIES)
    client.get_flow_hosts_series(top_n=3, step=300000)
    params = qs(responses.calls[0].request.url)
    assert params["N"] == ["3"]
    assert params["step"] == ["300000"]
