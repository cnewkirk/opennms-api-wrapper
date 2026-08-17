"""Tests for DataChoicesMixin – /rest/datachoices."""
import json

import responses
from .conftest import V1
from .fixtures import (
    USAGE_STATISTICS_REPORT, USAGE_STATISTICS_STATUS,
    USAGE_STATISTICS_META, PRODUCT_UPDATE_STATUS,
)


@responses.activate
def test_get_usage_statistics_report(client):
    responses.add(responses.GET, f"{V1}/datachoices",
                  json=USAGE_STATISTICS_REPORT)
    result = client.get_usage_statistics_report()
    assert result["nodes"] == 42


@responses.activate
def test_get_usage_statistics_status(client):
    responses.add(responses.GET, f"{V1}/datachoices/status",
                  json=USAGE_STATISTICS_STATUS)
    result = client.get_usage_statistics_status()
    assert result["enabled"] is True


@responses.activate
def test_set_usage_statistics_status(client):
    responses.add(responses.POST, f"{V1}/datachoices/status",
                  status=202)
    client.set_usage_statistics_status(
        enabled=False, initial_notice_acknowledged=True)
    body = json.loads(responses.calls[0].request.body)
    assert body == {"enabled": False,
                    "initialNoticeAcknowledged": True}


@responses.activate
def test_get_usage_statistics_meta(client):
    responses.add(responses.GET, f"{V1}/datachoices/meta",
                  json=USAGE_STATISTICS_META)
    result = client.get_usage_statistics_meta()
    assert "systemId" in result


@responses.activate
def test_get_product_update_status(client):
    responses.add(responses.GET,
                  f"{V1}/datachoices/productupdate/status",
                  json=PRODUCT_UPDATE_STATUS)
    result = client.get_product_update_status()
    assert result["optedIn"] is False


@responses.activate
def test_set_product_update_status(client):
    responses.add(responses.POST,
                  f"{V1}/datachoices/productupdate/status",
                  status=202)
    client.set_product_update_status(opted_in=True)
    body = json.loads(responses.calls[0].request.body)
    assert body == {"optedIn": True}


@responses.activate
def test_submit_product_update_enrollment(client):
    responses.add(responses.POST,
                  f"{V1}/datachoices/productupdate/submit",
                  status=202)
    client.submit_product_update_enrollment(
        {"consent": True, "email": "noc@example.com"})
    body = json.loads(responses.calls[0].request.body)
    assert body["consent"] is True
