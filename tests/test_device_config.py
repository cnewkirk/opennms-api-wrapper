"""Tests for DeviceConfigMixin – /rest/device-config."""
import json
import responses
from .conftest import V1, qs
from .fixtures import DEVICE_CONFIG, DEVICE_CONFIG_LIST


@responses.activate
def test_get_device_configs_defaults(client):
    responses.add(responses.GET, f"{V1}/device-config",
                  json=DEVICE_CONFIG_LIST)
    result = client.get_device_configs()
    assert result["deviceConfigs"][0]["id"] == 901
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["10"]
    assert params["offset"] == ["0"]


@responses.activate
def test_get_device_configs_filters(client):
    responses.add(responses.GET, f"{V1}/device-config",
                  json=DEVICE_CONFIG_LIST)
    client.get_device_configs(
        limit=5,
        offset=10,
        order_by="createdTime",
        order="desc",
        device_name="router01",
        ip_address="192.168.1.1",
        config_type="default",
        created_after=1000000,
        created_before=2000000,
    )
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["5"]
    assert params["offset"] == ["10"]
    assert params["orderBy"] == ["createdTime"]
    assert params["order"] == ["desc"]
    assert params["deviceName"] == ["router01"]
    assert params["ipAddress"] == ["192.168.1.1"]
    assert params["configType"] == ["default"]
    assert params["createdAfter"] == ["1000000"]
    assert params["createdBefore"] == ["2000000"]


@responses.activate
def test_get_device_config(client):
    responses.add(responses.GET, f"{V1}/device-config/901",
                  json=DEVICE_CONFIG)
    result = client.get_device_config(901)
    assert result["id"] == 901
    assert result["deviceName"] == "router01.example.com"
    assert "/device-config/901" in responses.calls[0].request.url


@responses.activate
def test_get_device_config_by_interface(client):
    responses.add(responses.GET, f"{V1}/device-config/interface/101",
                  json=DEVICE_CONFIG_LIST)
    result = client.get_device_config_by_interface(101)
    assert result["deviceConfigs"][0]["ipInterfaceId"] == 101
    assert "/device-config/interface/101" in responses.calls[0].request.url


@responses.activate
def test_get_latest_device_configs_defaults(client):
    responses.add(responses.GET, f"{V1}/device-config/latest",
                  json=DEVICE_CONFIG_LIST)
    result = client.get_latest_device_configs()
    assert result["deviceConfigs"][0]["isLatest"] is True
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["10"]
    assert params["offset"] == ["0"]


@responses.activate
def test_get_latest_device_configs_filters(client):
    responses.add(responses.GET, f"{V1}/device-config/latest",
                  json=DEVICE_CONFIG_LIST)
    client.get_latest_device_configs(
        limit=25,
        order_by="deviceName",
        order="asc",
        search="router",
        status="SUCCEEDED",
    )
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["25"]
    assert params["orderBy"] == ["deviceName"]
    assert params["order"] == ["asc"]
    assert params["search"] == ["router"]
    assert params["status"] == ["SUCCEEDED"]


@responses.activate
def test_download_device_configs(client):
    # Non-numeric text/plain falls back to string, not int.
    body = b"! Cisco IOS config\nhostname router01\n"
    responses.add(responses.GET, f"{V1}/device-config/download",
                  body=body, content_type="text/plain")
    result = client.download_device_configs([901, 902])
    assert "/device-config/download" in responses.calls[0].request.url
    params = qs(responses.calls[0].request.url)
    assert params["id"] == ["901,902"]
    assert isinstance(result, str)
    assert "router01" in result


@responses.activate
def test_backup_device_config(client):
    responses.add(responses.POST, f"{V1}/device-config/backup",
                  status=202, json={"status": "submitted"})
    payload = [
        {
            "ipAddress": "192.168.1.1",
            "location": "Default",
            "serviceName": "DeviceConfig-default",
            "blocking": False,
        }
    ]
    result = client.backup_device_config(payload)
    req = responses.calls[0].request
    body = json.loads(req.body)
    assert body[0]["ipAddress"] == "192.168.1.1"
    assert body[0]["serviceName"] == "DeviceConfig-default"
    assert req.headers["Content-Type"] == "application/json"
    assert result["status"] == "submitted"
