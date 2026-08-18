"""Shared pytest fixtures and helpers."""
import json
from urllib.parse import urlparse, parse_qs

import pytest
import responses as _responses
import opennms_api_wrapper as opennms

BASE_URL = "http://opennms:8980"
V1 = f"{BASE_URL}/opennms/rest"
V2 = f"{BASE_URL}/opennms/api/v2"

FORM = "application/x-www-form-urlencoded"
XML = "application/xml"


def add_contract(method, url, consumes, status=204, json_body=None):
    """Register a mock that enforces the endpoint's documented
    Content-Type.

    OpenNMS dispatches on Content-Type and answers 415 Unsupported
    Media Type when a write endpoint receives a body type outside its
    documented ``@Consumes`` set (XML-only creates, form-encoded
    updates — see the REST API docs per endpoint). This helper
    mirrors that behavior so a wrapper method sending the wrong
    content type fails the test exactly as it fails against a real
    server.
    """
    def _callback(request):
        content_type = (request.headers.get("Content-Type") or "")
        if content_type.split(";")[0].strip() != consumes:
            return (415, {}, "Unsupported Media Type")
        if json_body is not None:
            return (status, {"Content-Type": "application/json"},
                    json.dumps(json_body))
        return (status, {}, "")
    _responses.add_callback(method, url, callback=_callback)


@pytest.fixture
def client():
    return opennms.OpenNMS(BASE_URL, "admin", "admin", verify_ssl=False)


def qs(url: str) -> dict:
    """Parse query string from *url* into ``{key: [value, ...]}``."""
    return parse_qs(urlparse(url).query)
