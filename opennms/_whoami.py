"""Whoami REST API – /rest/whoami."""


class WhoamiMixin:
    def get_whoami(self):
        """Return information about the currently authenticated user."""
        return self._get("whoami")
