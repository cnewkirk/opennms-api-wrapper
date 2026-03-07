"""Foreign Sources Configuration REST API – /rest/foreignSourcesConfig."""


class ForeignSourcesConfigMixin:
    def get_foreign_source_config_policies(self):
        """List available provisioning policies."""
        return self._get("foreignSourcesConfig/policies")

    def get_foreign_source_config_detectors(self):
        """List available service detectors."""
        return self._get("foreignSourcesConfig/detectors")

    def get_foreign_source_config_services(self, group_name: str):
        """List services available for a given provisioning group.

        Args:
            group_name: Foreign source / provisioning group name.
        """
        return self._get(
            f"foreignSourcesConfig/services/{group_name}")

    def get_foreign_source_config_assets(self):
        """List available asset fields."""
        return self._get("foreignSourcesConfig/assets")

    def get_foreign_source_config_categories(self):
        """List available surveillance categories."""
        return self._get("foreignSourcesConfig/categories")
