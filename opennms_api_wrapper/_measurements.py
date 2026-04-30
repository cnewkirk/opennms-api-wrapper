"""Measurements REST API – /rest/measurements."""
from ._base import _OpenNMSBase
from typing import Optional
from .types import MeasurementsQuery


class MeasurementsMixin(_OpenNMSBase):
    def get_measurements(
        self,
        resource_id: str,
        attribute: str,
        start: int = -14400000,
        end: int = 0,
        step: int = 300000,
        max_rows: int = 0,
        aggregation: str = "AVERAGE",
        fallback_attribute: Optional[str] = None,
    ):
        """Retrieve time-series values for a single attribute.

        Args:
            resource_id: OpenNMS resource ID string, e.g.
                ``"node[1].interfaceSnmp[eth0-04013f75f101]"``.
            attribute: RRD attribute name, e.g. ``"ifInOctets"``.
            start: Start time in milliseconds since epoch.  Negative values
                are relative to *end* (default ``-14400000`` = 4 hours ago).
            end: End time in ms since epoch.  ``0`` means now.
            step: Requested interval between rows in ms (default 5 min).
            max_rows: Max rows to return (0 = no limit).
            aggregation: Consolidation function: ``"AVERAGE"``, ``"MIN"``,
                or ``"MAX"``.
            fallback_attribute: Secondary attribute used when the primary
                doesn't exist.
        """
        params: dict = {
            "start": start,
            "end": end,
            "step": step,
            "maxrows": max_rows,
            "aggregation": aggregation,
        }
        if fallback_attribute:
            params["fallback-attribute"] = fallback_attribute
        return self._get(f"measurements/{resource_id}/{attribute}", params=params)

    def get_measurements_multi(self, query: MeasurementsQuery):
        """Retrieve measurements for multiple attributes with JEXL expressions.

        Args:
            query: Query dict with keys: ``start`` (int, ms epoch),
                ``end`` (int, ms epoch), ``step`` (int, ms interval),
                ``maxrows`` (int), ``source`` (list of source dicts with
                keys ``resourceId``, ``attribute``, ``label``,
                ``aggregation``, and optionally ``transient``),
                ``expression`` (list of dicts with ``label``, ``value``
                as JEXL expression, and ``transient``).

        Example::

            client.get_measurements_multi({
                "start": 1425881287182,
                "end":   1425967687182,
                "step":  300000,
                "source": [
                    {
                        "resourceId": "node[1].interfaceSnmp[eth0-04013f75f101]",
                        "attribute": "ifInOctets",
                        "label": "octetsIn",
                        "aggregation": "AVERAGE",
                        "transient": False,
                    }
                ],
                "expression": [
                    {"label": "bitsIn", "value": "octetsIn * 8", "transient": False}
                ],
            })
        """
        return self._post("measurements", json_data=query)
