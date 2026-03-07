"""KSC Reports REST API – /rest/ksc."""


class KscReportsMixin:
    def get_ksc_reports(self):
        """List all KSC reports (returns ID and label for each)."""
        return self._get("ksc")

    def get_ksc_report(self, report_id: int):
        """Get a specific KSC report by *report_id*."""
        return self._get(f"ksc/{report_id}")

    def get_ksc_report_count(self) -> int:
        """Return the total number of KSC reports."""
        return self._get("ksc/count")

    def create_ksc_report(self, report: dict):
        """Create a new KSC report.

        Args:
            report: KSC report definition dict. Example::

                {
                    "id": 0,
                    "label": "My Bandwidth Report",
                    "show_timespan_button": False,
                    "show_graphtype_button": False,
                    "graphs_per_line": 1,
                    "graphs": [
                        {
                            "title": "Core Switch Bandwidth",
                            "resourceId": "node[1].interfaceSnmp[eth0-04013f75f101]",
                            "timespan": "7_day",
                            "graphtype": "mib2.bits",
                        }
                    ],
                }
        """
        return self._post("ksc", json_data=report)

    def update_ksc_report(self, report_id: int, report: dict):
        """Modify an existing KSC report.

        Args:
            report_id: Database ID of the KSC report to update.
            report: Updated report definition dict (same structure as
                ``create_ksc_report()``).
        """
        return self._put(f"ksc/{report_id}", json_data=report)
