"""Base HTTP client for the OpenNMS REST API."""
import requests


class _OpenNMSBase:
    """Base class providing authenticated HTTP helpers."""

    def __init__(self, url: str, username: str, password: str,
                 verify_ssl: bool = True, timeout: int = 30):
        """Initialize base URLs, credentials, and a shared requests session.

        Args:
            url: Base URL of the OpenNMS server (e.g. ``"https://onms.example.com"``).
            username: OpenNMS username for HTTP Basic authentication.
            password: Password for HTTP Basic authentication.
            verify_ssl: When ``False`` SSL certificate verification is
                disabled. Defaults to ``True``.
            timeout: Socket timeout in seconds for all HTTP requests.
                Defaults to ``30``.  Pass ``None`` to disable.
        """
        base = url.rstrip("/")
        self._v1_url = f"{base}/opennms/rest"
        self._v2_url = f"{base}/opennms/api/v2"
        self._timeout = timeout
        self._session = requests.Session()
        self._session.auth = (username, password)
        self._session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
        })
        self._session.verify = verify_ssl

    def _url(self, path: str, v2: bool = False) -> str:
        """Build a full endpoint URL, using the v2 base if *v2* is True."""
        base = self._v2_url if v2 else self._v1_url
        return f"{base}/{path.lstrip('/')}"

    def _parse(self, resp: requests.Response):
        """Parse an HTTP response into a Python object.

        Returns a dict/list for JSON, int or str for text/plain, and None
        for empty 204 responses.  Raises ``requests.exceptions.HTTPError``
        on non-2xx status codes.
        """
        resp.raise_for_status()
        if not resp.content:
            return None
        ct = resp.headers.get("Content-Type", "")
        if "application/json" in ct:
            return resp.json()
        if "text/plain" in ct:
            text = resp.text.strip()
            try:
                return int(text)
            except ValueError:
                return text
        try:
            return resp.json()
        except Exception:
            return resp.text

    def _get(self, path: str, params: dict = None, v2: bool = False):
        """Send a GET request and return the parsed response."""
        resp = self._session.get(self._url(path, v2), params=params,
                                 timeout=self._timeout)
        return self._parse(resp)

    def _post(self, path: str, json_data=None, form_data: dict = None,
              params: dict = None, v2: bool = False):
        """Send a POST request and return the parsed response.

        Sends form-encoded data when *form_data* is provided, otherwise JSON.
        """
        url = self._url(path, v2)
        if form_data is not None:
            resp = self._session.post(url, data=form_data, params=params,
                                      headers={"Content-Type": "application/x-www-form-urlencoded"},
                                      timeout=self._timeout)
        else:
            resp = self._session.post(url, json=json_data, params=params,
                                      timeout=self._timeout)
        return self._parse(resp)

    def _put(self, path: str, json_data=None, form_data: dict = None,
             params: dict = None, v2: bool = False):
        """Send a PUT request and return the parsed response.

        Sends form-encoded data when *form_data* is provided, otherwise JSON.
        """
        url = self._url(path, v2)
        if form_data is not None:
            resp = self._session.put(url, data=form_data, params=params,
                                     headers={"Content-Type": "application/x-www-form-urlencoded"},
                                     timeout=self._timeout)
        else:
            resp = self._session.put(url, json=json_data, params=params,
                                     timeout=self._timeout)
        return self._parse(resp)

    def _delete(self, path: str, params: dict = None, v2: bool = False):
        """Send a DELETE request and return the parsed response."""
        resp = self._session.delete(self._url(path, v2), params=params,
                                    timeout=self._timeout)
        return self._parse(resp)
