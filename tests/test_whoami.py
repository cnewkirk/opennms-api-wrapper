"""Tests for WhoamiMixin – /rest/whoami."""
import responses
from .conftest import V1
from .fixtures import WHOAMI


@responses.activate
def test_get_whoami(client):
    responses.add(responses.GET, f"{V1}/whoami", json=WHOAMI)
    result = client.get_whoami()
    assert result["id"] == "admin"
    assert "ROLE_ADMIN" in result["roles"]
