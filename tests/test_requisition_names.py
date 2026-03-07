"""Tests for RequisitionNamesMixin – /rest/requisitionNames."""
import responses
from .conftest import V1
from .fixtures import REQUISITION_NAMES


@responses.activate
def test_get_requisition_names(client):
    responses.add(responses.GET, f"{V1}/requisitionNames",
                  json=REQUISITION_NAMES)
    result = client.get_requisition_names()
    assert "Routers" in result["foreign-source"]
    assert result["count"] == 3
