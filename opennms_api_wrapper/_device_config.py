"""Device Configuration REST API – /rest/device-config."""


class DeviceConfigMixin:
    def get_device_configs(self, limit: int = 10, offset: int = 0,
                           order_by: str = None, order: str = None,
                           device_name: str = None, ip_address: str = None,
                           config_type: str = None,
                           created_after: int = None,
                           created_before: int = None):
        """List all device configurations (sorted by lastUpdated by default).

        Args:
            limit: Max number of results to return. Use ``0`` for all.
            offset: Zero-based offset for pagination.
            order_by: Field name to sort by.
            order: Sort direction: ``"asc"`` or ``"desc"``.
            device_name: Filter by device hostname.
            ip_address: Filter by IP address.
            config_type: Filter by config type string.
            created_after: Filter to configs created after this ms epoch.
            created_before: Filter to configs created before this ms epoch.
        """
        params: dict = {"limit": limit, "offset": offset}
        if order_by:
            params["orderBy"] = order_by
        if order:
            params["order"] = order
        if device_name:
            params["deviceName"] = device_name
        if ip_address:
            params["ipAddress"] = ip_address
        if config_type:
            params["configType"] = config_type
        if created_after is not None:
            params["createdAfter"] = created_after
        if created_before is not None:
            params["createdBefore"] = created_before
        return self._get("device-config", params=params)

    def get_device_config(self, config_id: int):
        """Get device configuration for a specific database *config_id*."""
        return self._get(f"device-config/{config_id}")

    def get_device_config_by_interface(self, interface_id: int):
        """Get all configs for a specific *interface_id*."""
        return self._get(f"device-config/interface/{interface_id}")

    def get_latest_device_configs(self, limit: int = 10, offset: int = 0,
                                  order_by: str = None, order: str = None,
                                  search: str = None, status: str = None):
        """Return the latest config for all devices.

        Args:
            limit: Max number of results to return. Use ``0`` for all.
            offset: Zero-based offset for pagination.
            order_by: Field name to sort by.
            order: Sort direction: ``"asc"`` or ``"desc"``.
            search: Search term for device name / IP.
            status: Filter by backup status.
        """
        params: dict = {"limit": limit, "offset": offset}
        if order_by:
            params["orderBy"] = order_by
        if order:
            params["order"] = order
        if search:
            params["search"] = search
        if status:
            params["status"] = status
        return self._get("device-config/latest", params=params)

    def download_device_configs(self, config_ids: list):
        """Download configs for one or more *config_ids*.

        Args:
            config_ids: List of integer config IDs to download.
        """
        params = {"id": ",".join(str(i) for i in config_ids)}
        return self._get("device-config/download", params=params)

    def backup_device_config(self, backups: list):
        """Trigger a backup retrieval for one or more interfaces.

        Args:
            backups: List of backup request dicts. Each dict has keys:
                ``ipAddress`` (str): Interface IP address.
                ``location`` (str): Monitoring location name (e.g.
                ``"Default"``). ``serviceName`` (str): Service name (e.g.
                ``"DeviceConfig-default"``). ``blocking`` (bool): Whether
                to wait for the backup to complete. Example::

                    [
                        {
                            "ipAddress": "192.168.1.1",
                            "location": "Default",
                            "serviceName": "DeviceConfig-default",
                            "blocking": False,
                        }
                    ]
        """
        return self._post("device-config/backup", json_data=backups)
