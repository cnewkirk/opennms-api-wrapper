"""Metadata REST API v2 – /api/v2/nodes/{id}/metadata and sub-resources."""


class MetadataMixin:
    # ==================================================================
    # Node metadata
    # ==================================================================

    def get_node_metadata(self, node_id):
        """Get all metadata for *node_id*."""
        return self._get(f"nodes/{node_id}/metadata", v2=True)

    def get_node_metadata_context(self, node_id, context: str):
        """Get all metadata for *node_id* within *context*."""
        return self._get(f"nodes/{node_id}/metadata/{context}", v2=True)

    def get_node_metadata_value(self, node_id, context: str, key: str):
        """Get a specific metadata value for *node_id*."""
        return self._get(f"nodes/{node_id}/metadata/{context}/{key}", v2=True)

    def set_node_metadata(self, node_id, metadata: list):
        """Set metadata entries for *node_id*.

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            metadata: List of dicts with keys ``context``, ``key``,
                ``value``. Only user-defined contexts (prefixed ``X-``)
                can be modified.
        """
        return self._post(f"nodes/{node_id}/metadata", json_data=metadata,
                          v2=True)

    def set_node_metadata_value(self, node_id, context: str, key: str,
                                value: str):
        """Set a single metadata key/value for *node_id*.

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            context: Metadata context (must be user-defined, prefixed ``X-``).
            key: Metadata key name.
            value: Metadata value string.
        """
        return self._put(
            f"nodes/{node_id}/metadata/{context}/{key}/{value}", v2=True)

    def delete_node_metadata_context(self, node_id, context: str):
        """Delete all metadata in *context* for *node_id*."""
        return self._delete(f"nodes/{node_id}/metadata/{context}", v2=True)

    def delete_node_metadata_key(self, node_id, context: str, key: str):
        """Delete a specific metadata key for *node_id*."""
        return self._delete(f"nodes/{node_id}/metadata/{context}/{key}",
                            v2=True)

    # ==================================================================
    # Interface metadata
    # ==================================================================

    def get_interface_metadata(self, node_id, ip_interface: str):
        """Get all metadata for the interface *ip_interface* on *node_id*."""
        return self._get(
            f"nodes/{node_id}/ipinterfaces/{ip_interface}/metadata", v2=True)

    def get_interface_metadata_context(self, node_id, ip_interface: str,
                                       context: str):
        """Get metadata within *context* for the given interface."""
        return self._get(
            f"nodes/{node_id}/ipinterfaces/{ip_interface}/metadata/{context}",
            v2=True)

    def get_interface_metadata_value(self, node_id, ip_interface: str,
                                     context: str, key: str):
        """Get a specific metadata value for the given interface."""
        return self._get(
            f"nodes/{node_id}/ipinterfaces/{ip_interface}/metadata"
            f"/{context}/{key}",
            v2=True,
        )

    def set_interface_metadata(self, node_id, ip_interface: str,
                               metadata: list):
        """Set metadata for the given interface.

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            ip_interface: IP address of the interface.
            metadata: List of dicts with keys ``context``, ``key``, ``value``.
        """
        return self._post(
            f"nodes/{node_id}/ipinterfaces/{ip_interface}/metadata",
            json_data=metadata, v2=True)

    def set_interface_metadata_value(self, node_id, ip_interface: str,
                                     context: str, key: str, value: str):
        """Set a single metadata key/value for the given interface.

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            ip_interface: IP address of the interface.
            context: Metadata context (must be user-defined, prefixed ``X-``).
            key: Metadata key name.
            value: Metadata value string.
        """
        return self._put(
            f"nodes/{node_id}/ipinterfaces/{ip_interface}/metadata"
            f"/{context}/{key}/{value}",
            v2=True,
        )

    def delete_interface_metadata_context(self, node_id, ip_interface: str,
                                          context: str):
        """Delete all metadata in *context* for the given interface."""
        return self._delete(
            f"nodes/{node_id}/ipinterfaces/{ip_interface}/metadata/{context}",
            v2=True)

    def delete_interface_metadata_key(self, node_id, ip_interface: str,
                                      context: str, key: str):
        """Delete a specific metadata key for the given interface."""
        return self._delete(
            f"nodes/{node_id}/ipinterfaces/{ip_interface}/metadata"
            f"/{context}/{key}",
            v2=True,
        )

    # ==================================================================
    # Service metadata
    # ==================================================================

    def get_service_metadata(self, node_id, ip_interface: str, service: str):
        """Get all metadata for *service* on *ip_interface* of *node_id*."""
        return self._get(
            f"nodes/{node_id}/ipinterfaces/{ip_interface}"
            f"/services/{service}/metadata",
            v2=True,
        )

    def get_service_metadata_context(self, node_id, ip_interface: str,
                                     service: str, context: str):
        """Get metadata within *context* for the given service."""
        return self._get(
            f"nodes/{node_id}/ipinterfaces/{ip_interface}"
            f"/services/{service}/metadata/{context}",
            v2=True,
        )

    def get_service_metadata_value(self, node_id, ip_interface: str,
                                   service: str, context: str, key: str):
        """Get a specific metadata value for the given service."""
        return self._get(
            f"nodes/{node_id}/ipinterfaces/{ip_interface}"
            f"/services/{service}/metadata/{context}/{key}",
            v2=True,
        )

    def set_service_metadata(self, node_id, ip_interface: str, service: str,
                             metadata: list):
        """Set metadata for the given service.

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            ip_interface: IP address of the interface.
            service: Monitored service name.
            metadata: List of dicts with keys ``context``, ``key``, ``value``.
        """
        return self._post(
            f"nodes/{node_id}/ipinterfaces/{ip_interface}"
            f"/services/{service}/metadata",
            json_data=metadata, v2=True,
        )

    def set_service_metadata_value(self, node_id, ip_interface: str,
                                   service: str, context: str, key: str,
                                   value: str):
        """Set a single metadata key/value for the given service.

        Args:
            node_id: Node database ID or ``"foreignSource:foreignId"``.
            ip_interface: IP address of the interface.
            service: Monitored service name.
            context: Metadata context (must be user-defined, prefixed ``X-``).
            key: Metadata key name.
            value: Metadata value string.
        """
        return self._put(
            f"nodes/{node_id}/ipinterfaces/{ip_interface}"
            f"/services/{service}/metadata/{context}/{key}/{value}",
            v2=True,
        )

    def delete_service_metadata_context(self, node_id, ip_interface: str,
                                        service: str, context: str):
        """Delete all metadata in *context* for the given service."""
        return self._delete(
            f"nodes/{node_id}/ipinterfaces/{ip_interface}"
            f"/services/{service}/metadata/{context}",
            v2=True,
        )

    def delete_service_metadata_key(self, node_id, ip_interface: str,
                                    service: str, context: str, key: str):
        """Delete a specific metadata key for the given service."""
        return self._delete(
            f"nodes/{node_id}/ipinterfaces/{ip_interface}"
            f"/services/{service}/metadata/{context}/{key}",
            v2=True,
        )
