"""Logs REST API – /rest/logs."""
from __future__ import annotations
from ._base import _OpenNMSBase
from typing import Any, Optional


class LogsMixin(_OpenNMSBase):
    def get_log_files(self):
        """Get the names of the available OpenNMS log files.

        Requires the ``ADMIN`` role.

        Returns:
            List of log file names, e.g. ``["manager.log", ...]``.
        """
        return self._get("logs")

    def get_log_contents(self, filename: str,
                         lines: Optional[int] = None,
                         reverse: Optional[bool] = None):
        """Get the contents of a single OpenNMS log file.

        Requires the ``ADMIN`` role.

        Args:
            filename: Log file name (must end in ``.log``).
            lines: Maximum number of lines to return (server default
                5000, range 1–10000).
            reverse: Return the most recent lines first (server
                default ``True``).

        Returns:
            The log contents as raw text (the server labels the
            response ``application/json`` but sends plain log lines).
            Empty string when the file does not exist (204).
        """
        params: dict[str, Any] = {"f": filename}
        if lines is not None:
            params["n"] = lines
        if reverse is not None:
            params["reverse"] = reverse
        return self._get_text("logs/contents", params=params)
