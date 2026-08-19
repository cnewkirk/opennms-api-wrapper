"""KSC Reports REST API – /rest/ksc."""
from __future__ import annotations
from xml.sax.saxutils import quoteattr

from ._base import _OpenNMSBase
from typing import Any, Optional
from .types import KscReport

_GRAPH_ATTRS = ("title", "timespan", "graphtype", "resourceId",
                "nodeId", "nodeSource", "domain", "interfaceId",
                "extlink")


def _attrs(data, keys) -> str:
    """Serialize *keys* of *data* as XML attributes."""
    parts = []
    for key in keys:
        if key in data:
            value = data[key]
            if isinstance(value, bool):
                value = str(value).lower()
            parts.append(f" {key}={quoteattr(str(value))}")
    return "".join(parts)


class KscReportsMixin(_OpenNMSBase):
    def get_ksc_reports(self):
        """List all KSC reports (returns ID and label for each)."""
        return self._get("ksc")

    def get_ksc_report(self, report_id: int):
        """Get a specific KSC report by *report_id*."""
        return self._get(f"ksc/{report_id}")

    def get_ksc_report_count(self) -> int:
        """Return the total number of KSC reports."""
        return self._get("ksc/count")

    def create_ksc_report(self, report: KscReport):
        """Create a new KSC report.

        The body is sent as XML — the KSC API documents "Create a
        report from an XML payload" with ``application/xml``.

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
        attrs = _attrs(report, ("id", "label", "show_timespan_button",
                                "show_graphtype_button",
                                "graphs_per_line"))
        graphs = "".join(
            f"<kscGraph{_attrs(graph, _GRAPH_ATTRS)}/>"
            for graph in report.get("graphs", []))
        xml = f"<kscReport{attrs}>{graphs}</kscReport>"
        return self._post_text("ksc", xml, "application/xml")

    def add_graph_to_ksc_report(self, report_id: int, report_name: str,
                                resource_id: str,
                                title: Optional[str] = None,
                                timespan: Optional[str] = None):
        """Add a graph to an existing KSC report.

        Mirrors ``PUT /rest/ksc/{reportid}``, which the KSC API
        documents as "Add a graph to the existing report with the
        given ID", built from query parameters.

        Args:
            report_id: Database ID of the KSC report.
            report_name: The graph definition's ``report.name`` from
                ``snmp-graph.properties.d``.
            resource_id: The time-series resource ID to graph.
            title: Optional graph title.
            timespan: Optional timespan (server default ``7_day``).
        """
        params: dict[str, Any] = {
            "reportName": report_name,
            "resourceId": resource_id,
        }
        if title is not None:
            params["title"] = title
        if timespan is not None:
            params["timespan"] = timespan
        return self._put(f"ksc/{report_id}", params=params)
