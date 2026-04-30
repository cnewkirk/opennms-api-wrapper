"""Secure Credentials Vault REST API – /rest/scv."""
from ._base import _OpenNMSBase
from .types import Credential


class ScvMixin(_OpenNMSBase):
    def get_credentials(self):
        """List all stored credentials."""
        return self._get("scv")

    def get_credential(self, alias: str):
        """Get a specific credential by *alias*.

        Args:
            alias: Credential alias (unique key).
        """
        return self._get(f"scv/{alias}")

    def create_credential(self, data: Credential):
        """Create a new credential entry.

        Args:
            data: Credential definition dict with keys ``alias``,
                ``username``, ``password``, and optionally ``attributes``.
        """
        return self._post("scv", json_data=data)

    def update_credential(self, alias: str, data: Credential):
        """Update an existing credential.

        Args:
            alias: Credential alias.
            data: Updated credential dict.
        """
        return self._put(f"scv/{alias}", json_data=data)

    def delete_credential(self, alias: str):
        """Delete a credential."""
        return self._delete(f"scv/{alias}")
