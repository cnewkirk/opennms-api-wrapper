"""Foreign Sources REST API – /rest/foreignSources."""


class ForeignSourcesMixin:
    # ==================================================================
    # Foreign Sources
    # ==================================================================

    def get_foreign_sources(self):
        """List all active (pending + deployed) foreign sources."""
        return self._get("foreignSources")

    def get_foreign_source(self, name: str):
        """Get a specific foreign source by *name*."""
        return self._get(f"foreignSources/{name}")

    def get_default_foreign_source(self):
        """Get the default foreign source definition."""
        return self._get("foreignSources/default")

    def get_deployed_foreign_sources(self):
        """List all deployed foreign sources."""
        return self._get("foreignSources/deployed")

    def get_deployed_foreign_source_count(self) -> int:
        """Return the count of deployed foreign sources."""
        return self._get("foreignSources/deployed/count")

    def create_foreign_source(self, foreign_source: dict):
        """Create a new foreign source.

        Args:
            foreign_source: Foreign source definition dict. Example::

                {
                    "name": "Servers",
                    "scan-interval": "1d",
                    "detectors": [
                        {
                            "name": "ICMP",
                            "class": "org.opennms.netmgt.provision.detector.icmp.IcmpDetector",
                            "parameter": [],
                        },
                        {
                            "name": "SNMP",
                            "class": "org.opennms.netmgt.provision.detector.snmp.SnmpDetector",
                            "parameter": [],
                        },
                    ],
                    "policies": [],
                }
        """
        return self._post("foreignSources", json_data=foreign_source)

    def update_foreign_source(self, name: str, foreign_source: dict):
        """Update an existing foreign source.

        Args:
            name: Foreign source name to update.
            foreign_source: Updated foreign source definition dict.
        """
        return self._put(f"foreignSources/{name}", json_data=foreign_source)

    def delete_foreign_source(self, name: str):
        """Delete a foreign source."""
        return self._delete(f"foreignSources/{name}")

    # ==================================================================
    # Detectors
    # ==================================================================

    def get_foreign_source_detectors(self, name: str):
        """List detectors for foreign source *name*."""
        return self._get(f"foreignSources/{name}/detectors")

    def get_foreign_source_detector(self, name: str, detector: str):
        """Get a specific detector from foreign source *name*."""
        return self._get(f"foreignSources/{name}/detectors/{detector}")

    def add_foreign_source_detector(self, name: str, detector: dict):
        """Add a detector to foreign source *name*.

        Args:
            name: Foreign source name.
            detector: Detector definition dict. Example:
                ``{"name": "HTTP", "class": "org.opennms.netmgt.provision.detector.web.HttpDetector", "parameter": []}``
        """
        return self._post(f"foreignSources/{name}/detectors", json_data=detector)

    def delete_foreign_source_detector(self, name: str, detector: str):
        """Remove a detector from foreign source *name*."""
        return self._delete(f"foreignSources/{name}/detectors/{detector}")

    # ==================================================================
    # Policies
    # ==================================================================

    def get_foreign_source_policies(self, name: str):
        """List policies for foreign source *name*."""
        return self._get(f"foreignSources/{name}/policies")

    def get_foreign_source_policy(self, name: str, policy: str):
        """Get a specific policy from foreign source *name*."""
        return self._get(f"foreignSources/{name}/policies/{policy}")

    def add_foreign_source_policy(self, name: str, policy: dict):
        """Add a policy to foreign source *name*.

        Args:
            name: Foreign source name.
            policy: Policy definition dict. Example::

                {
                    "name": "Do Not Persist Discovered IPs",
                    "class": "org.opennms.netmgt.provision.persist.policies.MatchingIpInterfacePolicy",
                    "parameter": [{"key": "action", "value": "DO_NOT_PERSIST"}],
                }
        """
        return self._post(f"foreignSources/{name}/policies", json_data=policy)

    def delete_foreign_source_policy(self, name: str, policy: str):
        """Remove a policy from foreign source *name*."""
        return self._delete(f"foreignSources/{name}/policies/{policy}")
