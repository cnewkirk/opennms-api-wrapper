"""Tests for retry adapter configuration."""
import opennms_api_wrapper as opennms
from urllib3.util.retry import Retry

BASE_URL = "http://opennms:8980"


def _get_retry(client, prefix="http://"):
    """Extract the Retry config from the adapter mounted on *prefix*."""
    adapter = client._session.get_adapter(prefix)
    return adapter.max_retries


class TestDefaultRetries:
    """Default client mounts a retry adapter with total=3."""

    def test_http_adapter_total(self):
        client = opennms.OpenNMS(BASE_URL, "admin", "admin",
                                 verify_ssl=False)
        retry = _get_retry(client, "http://")
        assert isinstance(retry, Retry)
        assert retry.total == 3

    def test_https_adapter_total(self):
        client = opennms.OpenNMS(BASE_URL, "admin", "admin",
                                 verify_ssl=False)
        retry = _get_retry(client, "https://")
        assert isinstance(retry, Retry)
        assert retry.total == 3

    def test_backoff_factor(self):
        client = opennms.OpenNMS(BASE_URL, "admin", "admin",
                                 verify_ssl=False)
        retry = _get_retry(client, "http://")
        assert retry.backoff_factor == 0.5

    def test_status_forcelist(self):
        client = opennms.OpenNMS(BASE_URL, "admin", "admin",
                                 verify_ssl=False)
        retry = _get_retry(client, "http://")
        assert set(retry.status_forcelist) == {500, 502, 503, 504}


class TestRetriesDisabled:
    """retries=0 mounts the pool adapter with max_retries=0 (no retries)."""

    def test_no_retry_adapter(self):
        client = opennms.OpenNMS(BASE_URL, "admin", "admin",
                                 verify_ssl=False, retries=0)
        retry = _get_retry(client, "http://")
        total = retry.total if isinstance(retry, Retry) else retry
        assert total == 0


class TestCustomRetries:
    """Custom retries=5 is propagated to the adapter."""

    def test_custom_total(self):
        client = opennms.OpenNMS(BASE_URL, "admin", "admin",
                                 verify_ssl=False, retries=5)
        retry = _get_retry(client, "http://")
        assert isinstance(retry, Retry)
        assert retry.total == 5

    def test_custom_https(self):
        client = opennms.OpenNMS(BASE_URL, "admin", "admin",
                                 verify_ssl=False, retries=5)
        retry = _get_retry(client, "https://")
        assert isinstance(retry, Retry)
        assert retry.total == 5
