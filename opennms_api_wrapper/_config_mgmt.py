"""Configuration Management REST API – /rest/cm."""
from ._base import _OpenNMSBase


class ConfigMgmtMixin(_OpenNMSBase):
    def get_config_names(self):
        """List all configuration names."""
        return self._get("cm")

    def get_config_schemas(self):
        """List all configuration schemas."""
        return self._get("cm/schema")

    def get_config_schema(self, name: str):
        """Get the schema for a specific configuration.

        Args:
            name: Configuration name.
        """
        return self._get(f"cm/schema/{name}")

    def get_config_ids(self, name: str):
        """List configuration IDs for a given configuration name.

        Args:
            name: Configuration name.
        """
        return self._get(f"cm/{name}")

    def get_config(self, name: str, config_id: str):
        """Get a specific configuration.

        Args:
            name: Configuration name.
            config_id: Configuration identifier.
        """
        return self._get(f"cm/{name}/{config_id}")

    def get_config_part(self, name: str, config_id: str, path: str):
        """Get a sub-part of a configuration.

        Args:
            name: Configuration name.
            config_id: Configuration identifier.
            path: Sub-path within the configuration.
        """
        return self._get(f"cm/{name}/{config_id}/{path}")

    def create_config(self, name: str, config_id: str, data: dict):
        """Create a new configuration.

        Args:
            name: Configuration name.
            config_id: Configuration identifier.
            data: Configuration data dict.
        """
        return self._post(f"cm/{name}/{config_id}", json_data=data)

    def update_config(self, name: str, config_id: str, data: dict):
        """Update a configuration.

        Args:
            name: Configuration name.
            config_id: Configuration identifier.
            data: Updated configuration data dict.
        """
        return self._put(f"cm/{name}/{config_id}", json_data=data)

    def delete_config(self, name: str, config_id: str):
        """Delete a configuration.

        Args:
            name: Configuration name.
            config_id: Configuration identifier.
        """
        return self._delete(f"cm/{name}/{config_id}")

    def delete_config_part(self, name: str, config_id: str,
                           path: str):
        """Delete a sub-part of a configuration.

        Args:
            name: Configuration name.
            config_id: Configuration identifier.
            path: Sub-path within the configuration.
        """
        return self._delete(f"cm/{name}/{config_id}/{path}")
