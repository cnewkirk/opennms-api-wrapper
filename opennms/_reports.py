"""Reports REST API – /rest/reports."""
from __future__ import annotations
from ._base import _OpenNMSBase
from typing import Any, Optional
from .types import ReportParameter, ReportDeliveryOptions


class ReportsMixin(_OpenNMSBase):
    # ------------------------------------------------------------------
    # Templates
    # ------------------------------------------------------------------

    def get_report_templates(self):
        """Get all available report templates."""
        return self._get("reports")

    def get_report_template(self, report_id: str,
                            user_id: Optional[str] = None):
        """Get the details of a report template.

        Args:
            report_id: Report template identifier.
            user_id: Optional user the template details are resolved
                for.
        """
        params = {"userId": user_id} if user_id else None
        return self._get(f"reports/{report_id}", params=params)

    def run_report(self, report_id: str, format: str,
                   parameters: list[ReportParameter]) -> bytes:
        """Run a report immediately and return the rendered output.

        Args:
            report_id: Report template identifier.
            format: Output format, e.g. ``"PDF"``, ``"SVG"``,
                ``"CSV"``, or ``"HTML"``.
            parameters: Report parameter dicts with ``name``, ``type``,
                and ``value`` keys.

        Returns:
            The rendered report (e.g. PDF or CSV data).
        """
        body = {"format": format, "parameters": parameters}
        return self._post_bytes(f"reports/{report_id}", json_data=body)

    # ------------------------------------------------------------------
    # Persisted reports
    # ------------------------------------------------------------------

    def get_persisted_reports(self):
        """Get all persisted (stored) report instances."""
        return self._get("reports/persisted")

    def deliver_report(self, report_id: str, format: str,
                       parameters: list[ReportParameter],
                       delivery_options: ReportDeliveryOptions):
        """Run a report and deliver it (email, webhook, or persist).

        Args:
            report_id: Report template identifier.
            format: Output format, e.g. ``"PDF"`` or ``"CSV"``.
            parameters: Report parameter dicts with ``name``, ``type``,
                and ``value`` keys.
            delivery_options: Delivery options dict; ``instanceId``
                is required.
        """
        body = {
            "id": report_id,
            "format": format,
            "parameters": parameters,
            "deliveryOptions": delivery_options,
        }
        return self._post("reports/persisted", json_data=body)

    def download_report(self, locator_id: int,
                        format: Optional[str] = None) -> bytes:
        """Download a persisted report.

        Args:
            locator_id: Catalog identifier of the persisted report.
            format: Optional format to re-render the report in.

        Returns:
            The rendered report (e.g. PDF or CSV data).
        """
        params: dict[str, Any] = {"locatorId": locator_id}
        if format is not None:
            params["format"] = format
        return self._get_bytes("reports/download", params=params)

    def delete_persisted_reports(self):
        """Delete all persisted reports."""
        return self._delete("reports/persisted")

    def delete_persisted_report(self, report_id: int):
        """Delete a persisted report by its catalog identifier.

        Args:
            report_id: Catalog identifier of the persisted report.
        """
        return self._delete(f"reports/persisted/{report_id}")

    # ------------------------------------------------------------------
    # Scheduled reports
    # ------------------------------------------------------------------

    def get_scheduled_reports(self):
        """Get all scheduled report triggers."""
        return self._get("reports/scheduled")

    def get_scheduled_report(self, trigger_name: str):
        """Get the details of a scheduled report trigger.

        Args:
            trigger_name: Name of the scheduled report trigger.
        """
        return self._get(f"reports/scheduled/{trigger_name}")

    def schedule_report(self, report_id: str, format: str,
                        cron_expression: str,
                        parameters: list[ReportParameter],
                        delivery_options: ReportDeliveryOptions):
        """Create a scheduled report.

        Args:
            report_id: Report template identifier.
            format: Output format, e.g. ``"PDF"`` or ``"CSV"``.
            cron_expression: Quartz cron expression for the schedule.
            parameters: Report parameter dicts with ``name``, ``type``,
                and ``value`` keys.
            delivery_options: Delivery options dict; ``instanceId``
                is required.
        """
        body = {
            "id": report_id,
            "format": format,
            "cronExpression": cron_expression,
            "parameters": parameters,
            "deliveryOptions": delivery_options,
        }
        return self._post("reports/scheduled", json_data=body)

    def update_scheduled_report(self, trigger_name: str, data: dict):
        """Update an existing scheduled report trigger.

        Args:
            trigger_name: Name of the scheduled report trigger.
            data: Updated trigger definition (``parameters``,
                ``deliveryOptions``, ``cronExpression``).
        """
        return self._put(f"reports/scheduled/{trigger_name}",
                         json_data=data)

    def delete_scheduled_reports(self):
        """Delete all scheduled report triggers."""
        return self._delete("reports/scheduled")

    def delete_scheduled_report(self, trigger_name: str):
        """Delete a scheduled report trigger by name.

        Args:
            trigger_name: Name of the scheduled report trigger.
        """
        return self._delete(f"reports/scheduled/{trigger_name}")
