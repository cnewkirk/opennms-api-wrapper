"""Tests for ClassificationsMixin – /rest/classifications."""
import json
import responses
from .conftest import V1, qs
from .fixtures import (
    CLASSIFICATION_RULE, CLASSIFICATION_RULE_LIST,
    CLASSIFICATION_GROUP, CLASSIFICATION_GROUP_LIST,
    CLASSIFY_RESULT, CLASSIFICATION_PROTOCOLS,
)


@responses.activate
def test_get_classification_rules(client):
    responses.add(responses.GET, f"{V1}/classifications",
                  json=CLASSIFICATION_RULE_LIST)
    result = client.get_classification_rules()
    assert result["classificationRule"][0]["name"] == "HTTPS"


@responses.activate
def test_get_classification_rule(client):
    responses.add(responses.GET, f"{V1}/classifications/1",
                  json=CLASSIFICATION_RULE)
    result = client.get_classification_rule(1)
    assert result["id"] == 1


@responses.activate
def test_create_classification_rule(client):
    responses.add(responses.POST, f"{V1}/classifications", status=201)
    rule = {"name": "SSH", "dstPort": "22", "protocol": "tcp"}
    client.create_classification_rule(rule)
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "SSH"


@responses.activate
def test_update_classification_rule(client):
    responses.add(responses.PUT, f"{V1}/classifications/1", status=204)
    client.update_classification_rule(1, {"name": "HTTPS", "dstPort": "443"})
    body = json.loads(responses.calls[0].request.body)
    assert body["dstPort"] == "443"


@responses.activate
def test_delete_classification_rules_by_group(client):
    responses.add(responses.DELETE, f"{V1}/classifications", status=204)
    client.delete_classification_rules(group_id=1)
    params = qs(responses.calls[0].request.url)
    assert params["groupId"] == ["1"]


@responses.activate
def test_delete_classification_rule(client):
    responses.add(responses.DELETE, f"{V1}/classifications/1", status=204)
    result = client.delete_classification_rule(1)
    assert result is None


@responses.activate
def test_classify(client):
    responses.add(responses.POST, f"{V1}/classifications/classify",
                  json=CLASSIFY_RESULT)
    req = {"dstPort": "443", "protocol": "tcp"}
    result = client.classify(req)
    assert result["classification"] == "HTTPS"


@responses.activate
def test_get_classification_groups(client):
    responses.add(responses.GET, f"{V1}/classifications/groups",
                  json=CLASSIFICATION_GROUP_LIST)
    result = client.get_classification_groups()
    assert result["classificationGroup"][0]["name"] == "default"


@responses.activate
def test_get_classification_group(client):
    responses.add(responses.GET, f"{V1}/classifications/groups/1",
                  json=CLASSIFICATION_GROUP)
    result = client.get_classification_group(1)
    assert result["id"] == 1


@responses.activate
def test_create_classification_group(client):
    responses.add(responses.POST, f"{V1}/classifications/groups",
                  status=201)
    client.create_classification_group({"name": "custom"})
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "custom"


@responses.activate
def test_update_classification_group(client):
    responses.add(responses.PUT, f"{V1}/classifications/groups/1",
                  status=204)
    client.update_classification_group(1, {"name": "renamed"})
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "renamed"


@responses.activate
def test_delete_classification_group(client):
    responses.add(responses.DELETE, f"{V1}/classifications/groups/1",
                  status=204)
    result = client.delete_classification_group(1)
    assert result is None


@responses.activate
def test_import_classification_rules(client):
    responses.add(responses.POST, f"{V1}/classifications/groups/1",
                  status=204)
    csv = "name;dstPort;protocol\\nSSH;22;tcp"
    result = client.import_classification_rules(1, csv)
    assert result is None
    assert responses.calls[0].request.headers["Content-Type"] == \
        "text/comma-separated-values"


@responses.activate
def test_get_classification_protocols(client):
    responses.add(responses.GET, f"{V1}/classifications/protocols",
                  json=CLASSIFICATION_PROTOCOLS)
    result = client.get_classification_protocols()
    assert "TCP" in result
