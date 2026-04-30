"""Base HTTP client for the OpenNMS REST API."""
from __future__ import annotations
from typing import Any, Optional
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError
from urllib3.util.retry import Retry

from ._exceptions import (
    BadRequestError, AuthenticationError, ForbiddenError,
    NotFoundError, ConflictError, ServerError, OpenNMSHTTPError,
)


class _OpenNMSBase:
    """Base class providing authenticated HTTP helpers."""

    def __init__(self, url: str, username: str, password: str,
                 verify_ssl: bool = True, timeout: int = 30,
                 retries: int = 3):
        """Initialize base URLs, credentials, and a shared requests session.

        Args:
            url: Base URL of the OpenNMS server (e.g. ``"https://onms.example.com"``).
            username: OpenNMS username for HTTP Basic authentication.
            password: Password for HTTP Basic authentication.
            verify_ssl: When ``False`` SSL certificate verification is
                disabled. Defaults to ``True``.
            timeout: Read timeout in seconds for all HTTP requests.
                The connect timeout is capped at ``min(timeout, 10)``
                seconds so unreachable hosts fail fast.
                Defaults to ``30``.  Pass ``None`` to disable.
            retries: Number of retries on connection errors and
                HTTP 500/502/503/504.  Uses exponential backoff with
                a 0.5 s factor.  Pass ``0`` to disable retries.
        """
        base = url.rstrip("/")
        self._v1_url = f"{base}/opennms/rest"
        self._v2_url = f"{base}/opennms/api/v2"
        self._timeout = (min(timeout, 10), timeout) if timeout is not None else None
        self._session = requests.Session()
        self._session.auth = (username, password)
        self._session.headers.update({
            "Accept": "application/json, text/plain;q=0.9",
            "Content-Type": "application/json",
        })
        self._session.verify = verify_ssl
        retry = Retry(
            total=retries,
            backoff_factor=0.5,
            status_forcelist=(500, 502, 503, 504),
            allowed_methods=None,
            raise_on_status=False,
        ) if retries > 0 else 0
        adapter = HTTPAdapter(
            pool_connections=4, pool_maxsize=20, max_retries=retry
        )
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

    def _url(self, path: str, v2: bool = False) -> str:
        """Build a full endpoint URL, using the v2 base if *v2* is True."""
        base = self._v2_url if v2 else self._v1_url
        return f"{base}/{path.lstrip('/')}"

    def _raise_for_status(self, resp: requests.Response) -> None:
        """Translate an HTTP error response into a library exception."""
        try:
            resp.raise_for_status()
        except HTTPError as exc:
            status = resp.status_code
            msg = str(exc)
            if status == 400:
                raise BadRequestError(msg, resp) from exc
            if status == 401:
                raise AuthenticationError(msg, resp) from exc
            if status == 403:
                raise ForbiddenError(msg, resp) from exc
            if status == 404:
                raise NotFoundError(msg, resp) from exc
            if status == 409:
                raise ConflictError(msg, resp) from exc
            if 500 <= status < 600:
                raise ServerError(msg, resp) from exc
            raise OpenNMSHTTPError(msg, resp) from exc

    def _parse(self, resp: requests.Response):
        """Parse an HTTP response into a Python object.

        Returns a dict/list for JSON, int or str for text/plain, and None
        for empty 204 responses.  Raises an :class:`OpenNMSHTTPError`
        subclass on non-2xx status codes.
        """
        self._raise_for_status(resp)
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

    def _get(self, path: str, params: Optional[dict[str, Any]] = None, v2: bool = False):
        """Send a GET request and return the parsed response."""
        resp = self._session.get(self._url(path, v2), params=params,
                                 timeout=self._timeout)
        return self._parse(resp)

    def _post(self, path: str, json_data=None, form_data: Optional[Any] = None,
              params: Optional[dict[str, Any]] = None, v2: bool = False):
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

    def _put(self, path: str, json_data=None, form_data: Optional[Any] = None,
             params: Optional[dict[str, Any]] = None, v2: bool = False):
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

    def _delete(self, path: str, params: Optional[dict[str, Any]] = None, json_data=None,
                v2: bool = False):
        """Send a DELETE request and return the parsed response."""
        resp = self._session.delete(self._url(path, v2), params=params,
                                    json=json_data, timeout=self._timeout)
        return self._parse(resp)

    def _patch(self, path: str, json_data=None, params: Optional[dict[str, Any]] = None,
               v2: bool = False):
        """Send a PATCH request and return the parsed response."""
        resp = self._session.patch(self._url(path, v2), json=json_data,
                                   params=params, timeout=self._timeout)
        return self._parse(resp)

    def _get_text(self, path: str, v2: bool = False) -> str:
        """Send a GET request and return the raw response text."""
        resp = self._session.get(self._url(path, v2),
                                 timeout=self._timeout)
        self._raise_for_status(resp)
        return resp.text

    def _post_files(self, path: str, files: dict,
                    v2: bool = False):
        """Send a POST request with multipart file upload."""
        resp = self._session.post(self._url(path, v2), files=files,
                                  timeout=self._timeout)
        return self._parse(resp)

    def _post_text(self, path: str, data: str, content_type: str,
                   v2: bool = False):
        """Send a POST request with a raw text body."""
        resp = self._session.post(
            self._url(path, v2), data=data,
            headers={"Content-Type": content_type},
            timeout=self._timeout)
        return self._parse(resp)
