"""Shared pytest fixtures and helpers."""
from urllib.parse import urlparse, parse_qs

import pytest
import opennms_api_wrapper as opennms

BASE_URL = "http://opennms:8980"
V1 = f"{BASE_URL}/opennms/rest"
V2 = f"{BASE_URL}/opennms/api/v2"


@pytest.fixture
def client():
    return opennms.OpenNMS(BASE_URL, "admin", "admin", verify_ssl=False)


def qs(url: str) -> dict:
    """Parse query string from *url* into ``{key: [value, ...]}``."""
    return parse_qs(urlparse(url).query)
