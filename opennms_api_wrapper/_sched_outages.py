"""Scheduled Outages REST API – /rest/sched-outages."""


class SchedOutagesMixin:
    # ==================================================================
    # Scheduled Outages CRUD
    # ==================================================================

    def get_sched_outages(self):
        """List all configured scheduled outages."""
        return self._get("sched-outages")

    def get_sched_outage(self, outage_name: str):
        """Get a specific scheduled outage by *outage_name*."""
        return self._get(f"sched-outages/{outage_name}")

    def create_sched_outage(self, outage: dict):
        """Add a new (or replace an existing) scheduled outage.

        Args:
            outage: Scheduled outage definition dict. Valid ``type`` values:
                ``"weekly"``, ``"monthly"``, ``"specific"``, ``"daily"``.
                For ``"weekly"`` outages the ``"day"`` key in each time
                entry is the weekday name (lowercase). For ``"monthly"``
                outages ``"day"`` is an integer day-of-month. For
                ``"specific"`` outages ``"begins"`` and ``"ends"`` are
                full datetime strings (``"DD-Mon-YYYY HH:MM:SS"``).
                Example::

                    {
                        "name": "Weekend-Maintenance",
                        "type": "weekly",
                        "time": [
                            {"day": "saturday", "begins": "00:00:00", "ends": "23:59:59"},
                            {"day": "sunday",   "begins": "00:00:00", "ends": "23:59:59"},
                        ],
                        "node": [{"id": 1}, {"id": 2}],
                        "interface": [{"address": "192.168.0.1"}],
                    }
        """
        return self._post("sched-outages", json_data=outage)

    def delete_sched_outage(self, outage_name: str):
        """Delete a scheduled outage."""
        return self._delete(f"sched-outages/{outage_name}")

    # ==================================================================
    # Daemon associations
    # ==================================================================

    def associate_sched_outage_collectd(self, outage_name: str, package: str):
        """Associate outage *outage_name* with collectd *package*."""
        return self._put(f"sched-outages/{outage_name}/collectd/{package}")

    def dissociate_sched_outage_collectd(self, outage_name: str, package: str):
        """Remove collectd *package* association from *outage_name*."""
        return self._delete(f"sched-outages/{outage_name}/collectd/{package}")

    def associate_sched_outage_pollerd(self, outage_name: str, package: str):
        """Associate outage *outage_name* with pollerd *package*."""
        return self._put(f"sched-outages/{outage_name}/pollerd/{package}")

    def dissociate_sched_outage_pollerd(self, outage_name: str, package: str):
        """Remove pollerd *package* association from *outage_name*."""
        return self._delete(f"sched-outages/{outage_name}/pollerd/{package}")

    def associate_sched_outage_threshd(self, outage_name: str, package: str):
        """Associate outage *outage_name* with threshd *package*."""
        return self._put(f"sched-outages/{outage_name}/threshd/{package}")

    def dissociate_sched_outage_threshd(self, outage_name: str, package: str):
        """Remove threshd *package* association from *outage_name*."""
        return self._delete(f"sched-outages/{outage_name}/threshd/{package}")

    def associate_sched_outage_notifd(self, outage_name: str):
        """Associate outage *outage_name* with the notifications daemon."""
        return self._put(f"sched-outages/{outage_name}/notifd")

    def dissociate_sched_outage_notifd(self, outage_name: str):
        """Remove notifications daemon association from *outage_name*."""
        return self._delete(f"sched-outages/{outage_name}/notifd")
