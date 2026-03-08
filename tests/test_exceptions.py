"""Tests for the exception hierarchy raised on HTTP error responses."""
import pytest
import responses as rsps

import opennms_api_wrapper as opennms
from tests.conftest import V1, V2


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _alarm_url():
    return f"{V1}/alarms"


# ---------------------------------------------------------------------------
# Exception class structure
# ---------------------------------------------------------------------------

def test_exception_hierarchy():
    assert issubclass(opennms.OpenNMSHTTPError, opennms.OpenNMSError)
    assert issubclass(opennms.BadRequestError,    opennms.OpenNMSHTTPError)
    assert issubclass(opennms.AuthenticationError, opennms.OpenNMSHTTPError)
    assert issubclass(opennms.ForbiddenError,     opennms.OpenNMSHTTPError)
    assert issubclass(opennms.NotFoundError,      opennms.OpenNMSHTTPError)
    assert issubclass(opennms.ConflictError,      opennms.OpenNMSHTTPError)
    assert issubclass(opennms.ServerError,        opennms.OpenNMSHTTPError)


def test_all_exported():
    names = [
        "OpenNMSError", "OpenNMSHTTPError", "BadRequestError",
        "AuthenticationError", "ForbiddenError", "NotFoundError",
        "ConflictError", "ServerError",
    ]
    for name in names:
        assert hasattr(opennms, name), f"opennms.{name} not exported"


# ---------------------------------------------------------------------------
# status_code and response attributes
# ---------------------------------------------------------------------------

@rsps.activate
def test_not_found_attributes(client):
    rsps.add(rsps.GET, _alarm_url(), status=404)
    with pytest.raises(opennms.NotFoundError) as exc_info:
        client.get_alarms()
    err = exc_info.value
    assert err.status_code == 404
    assert err.response is not None
    assert err.response.status_code == 404


# ---------------------------------------------------------------------------
# One test per mapped status code
# ---------------------------------------------------------------------------

@rsps.activate
def test_400_raises_bad_request(client):
    rsps.add(rsps.GET, _alarm_url(), status=400)
    with pytest.raises(opennms.BadRequestError) as exc_info:
        client.get_alarms()
    assert exc_info.value.status_code == 400


@rsps.activate
def test_401_raises_authentication_error(client):
    rsps.add(rsps.GET, _alarm_url(), status=401)
    with pytest.raises(opennms.AuthenticationError) as exc_info:
        client.get_alarms()
    assert exc_info.value.status_code == 401


@rsps.activate
def test_403_raises_forbidden(client):
    rsps.add(rsps.GET, _alarm_url(), status=403)
    with pytest.raises(opennms.ForbiddenError) as exc_info:
        client.get_alarms()
    assert exc_info.value.status_code == 403


@rsps.activate
def test_404_raises_not_found(client):
    rsps.add(rsps.GET, _alarm_url(), status=404)
    with pytest.raises(opennms.NotFoundError) as exc_info:
        client.get_alarms()
    assert exc_info.value.status_code == 404


@rsps.activate
def test_409_raises_conflict(client):
    rsps.add(rsps.GET, _alarm_url(), status=409)
    with pytest.raises(opennms.ConflictError) as exc_info:
        client.get_alarms()
    assert exc_info.value.status_code == 409


@rsps.activate
def test_500_raises_server_error(client):
    rsps.add(rsps.GET, _alarm_url(), status=500)
    with pytest.raises(opennms.ServerError) as exc_info:
        client.get_alarms()
    assert exc_info.value.status_code == 500


@rsps.activate
def test_503_raises_server_error(client):
    rsps.add(rsps.GET, _alarm_url(), status=503)
    with pytest.raises(opennms.ServerError) as exc_info:
        client.get_alarms()
    assert exc_info.value.status_code == 503


@rsps.activate
def test_unknown_4xx_raises_http_error(client):
    rsps.add(rsps.GET, _alarm_url(), status=422)
    with pytest.raises(opennms.OpenNMSHTTPError) as exc_info:
        client.get_alarms()
    assert exc_info.value.status_code == 422
    # Should NOT be a more-specific subclass
    assert type(exc_info.value) is opennms.OpenNMSHTTPError


# ---------------------------------------------------------------------------
# Catch-all via base class
# ---------------------------------------------------------------------------

@rsps.activate
def test_catch_via_base_class(client):
    rsps.add(rsps.GET, _alarm_url(), status=404)
    with pytest.raises(opennms.OpenNMSHTTPError):
        client.get_alarms()


@rsps.activate
def test_catch_via_opennms_error(client):
    rsps.add(rsps.GET, _alarm_url(), status=403)
    with pytest.raises(opennms.OpenNMSError):
        client.get_alarms()


# ---------------------------------------------------------------------------
# Works on v2 endpoints too
# ---------------------------------------------------------------------------

@rsps.activate
def test_v2_404_raises_not_found(client):
    rsps.add(rsps.GET, f"{V2}/alarms/99999", status=404)
    with pytest.raises(opennms.NotFoundError) as exc_info:
        client.get_alarm_v2(99999)
    assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# Works through _get_text (eventconf / classification raw-text paths)
# ---------------------------------------------------------------------------

@rsps.activate
def test_get_text_404_raises_not_found(client):
    rsps.add(rsps.GET, f"{V1}/classifications/protocols", status=404)
    with pytest.raises(opennms.NotFoundError) as exc_info:
        client.get_classification_protocols()
    assert exc_info.value.status_code == 404
