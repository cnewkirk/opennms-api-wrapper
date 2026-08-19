"""Discovery REST API v2 – /api/v2/discovery."""
from ._base import _OpenNMSBase


class DiscoveryMixin(_OpenNMSBase):
    def discover(self, config: dict):
        """Submit a one-time discovery scan configuration (v2).

        Args:
            config: Discovery configuration dict. Supported keys (all lists
                default to empty):

                - ``specifics`` (list): Individual IPs to scan. Each entry::

                      {"ip": "192.168.0.1", "location": "Default",
                       "retries": 1, "timeout": 2000, "foreignSource": "FS"}

                - ``include_ranges`` (list): IP ranges to scan. Each entry::

                      {"begin": "192.168.0.1", "end": "192.168.0.254",
                       "location": "Default", "retries": 1, "timeout": 2000}

                - ``exclude_ranges`` (list): IP ranges to exclude. Each entry::

                      {"begin": "192.168.0.100", "end": "192.168.0.110"}

                - ``include_urls`` (list): URLs with newline-delimited IPs.
                  Each entry::

                      {"url": "http://example.com/ips.txt", "location": "Default"}

        Note: The v2 discovery endpoint is documented as XML-only.  This
        method sends JSON; if your OpenNMS version rejects it with HTTP 415
        please open an issue — the workaround is to submit the request
        manually with an XML body matching the ``discovery-configuration``
        schema.

        Example::

            client.discover({
                "specifics": [
                    {"ip": "10.0.0.1", "location": "Default", "foreignSource": "Routers"}
                ],
                "include_ranges": [
                    {"begin": "10.0.1.1", "end": "10.0.1.254"}
                ],
            })
        """
        return self._post("discovery", json_data=config, v2=True)
