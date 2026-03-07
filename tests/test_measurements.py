"""Tests for MeasurementsMixin – /rest/measurements."""
import json
import responses
from .conftest import V1, qs
from .fixtures import MEASUREMENTS

RESOURCE_ID = "node[1].interfaceSnmp[eth0-04013f75f101]"
ATTRIBUTE = "ifInOctets"


@responses.activate
def test_get_measurements_defaults(client):
    responses.add(responses.GET,
                  f"{V1}/measurements/{RESOURCE_ID}/{ATTRIBUTE}",
                  json=MEASUREMENTS)
    result = client.get_measurements(RESOURCE_ID, ATTRIBUTE)
    assert result["labels"] == ["ifInOctets"]
    assert len(result["timestamps"]) == 3
    params = qs(responses.calls[0].request.url)
    assert params["start"] == ["-14400000"]
    assert params["end"] == ["0"]
    assert params["step"] == ["300000"]
    assert params["maxrows"] == ["0"]
    assert params["aggregation"] == ["AVERAGE"]


@responses.activate
def test_get_measurements_custom_params(client):
    responses.add(responses.GET,
                  f"{V1}/measurements/{RESOURCE_ID}/{ATTRIBUTE}",
                  json=MEASUREMENTS)
    client.get_measurements(
        RESOURCE_ID, ATTRIBUTE,
        start=1425580938256,
        end=1425588138256,
        step=60000,
        max_rows=800,
        aggregation="MAX",
        fallback_attribute="ifHCInOctets",
    )
    params = qs(responses.calls[0].request.url)
    assert params["start"] == ["1425580938256"]
    assert params["step"] == ["60000"]
    assert params["maxrows"] == ["800"]
    assert params["aggregation"] == ["MAX"]
    assert params["fallback-attribute"] == ["ifHCInOctets"]


@responses.activate
def test_get_measurements_multi(client):
    responses.add(responses.POST, f"{V1}/measurements", json=MEASUREMENTS)
    query = {
        "start": 1425580938256,
        "end": 1425588138256,
        "step": 300000,
        "source": [
            {
                "resourceId": RESOURCE_ID,
                "attribute": "ifInOctets",
                "label": "octetsIn",
                "aggregation": "AVERAGE",
                "transient": False,
            },
            {
                "resourceId": RESOURCE_ID,
                "attribute": "ifOutOctets",
                "label": "octetsOut",
                "aggregation": "AVERAGE",
                "transient": False,
            },
        ],
        "expression": [
            {
                "label": "bitsIn",
                "value": "octetsIn * 8",
                "transient": False,
            }
        ],
    }
    result = client.get_measurements_multi(query)
    assert result["labels"] == ["ifInOctets"]
    req = responses.calls[0].request
    assert req.method == "POST"
    body = json.loads(req.body)
    assert len(body["source"]) == 2
    assert body["expression"][0]["label"] == "bitsIn"
    assert req.headers["Content-Type"] == "application/json"
