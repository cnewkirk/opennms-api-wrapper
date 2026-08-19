"""Data Choices REST API – /rest/datachoices.

Controls the anonymous usage-statistics collection and product-update
enrollment settings.
"""
from __future__ import annotations
from ._base import _OpenNMSBase
from typing import Any, Optional
from .types import ProductUpdateEnrollment


class DataChoicesMixin(_OpenNMSBase):
    def get_usage_statistics_report(self):
        """Get the usage-statistics report for this system."""
        return self._get("datachoices")

    def get_usage_statistics_status(self):
        """Get the usage-statistics collection status.

        Returns:
            Dict with ``enabled`` and ``initialNoticeAcknowledged``
            keys.
        """
        return self._get("datachoices/status")

    def set_usage_statistics_status(
            self, enabled: Optional[bool] = None,
            initial_notice_acknowledged: Optional[bool] = None):
        """Update the usage-statistics collection status.

        Args:
            enabled: Enable or disable usage-statistics collection.
            initial_notice_acknowledged: Mark the initial notice as
                acknowledged.
        """
        body: dict[str, Any] = {}
        if enabled is not None:
            body["enabled"] = enabled
        if initial_notice_acknowledged is not None:
            body["initialNoticeAcknowledged"] = (
                initial_notice_acknowledged)
        return self._post("datachoices/status", json_data=body)

    def get_usage_statistics_meta(self):
        """Get metadata describing the usage-statistics fields."""
        return self._get("datachoices/meta")

    def get_product_update_status(self):
        """Get the product-update enrollment status.

        Returns:
            Dict with ``optedIn`` and ``noticeAcknowledged`` keys.
        """
        return self._get("datachoices/productupdate/status")

    def set_product_update_status(
            self, opted_in: Optional[bool] = None,
            notice_acknowledged: Optional[bool] = None):
        """Update the product-update enrollment status.

        Args:
            opted_in: Opt in to or out of product-update enrollment.
            notice_acknowledged: Mark the enrollment notice as
                acknowledged.
        """
        body: dict[str, Any] = {}
        if opted_in is not None:
            body["optedIn"] = opted_in
        if notice_acknowledged is not None:
            body["noticeAcknowledged"] = notice_acknowledged
        return self._post("datachoices/productupdate/status",
                          json_data=body)

    def submit_product_update_enrollment(
            self, form_data: ProductUpdateEnrollment):
        """Submit the product-update enrollment form.

        Args:
            form_data: Enrollment form dict (``consent``,
                ``firstName``, ``lastName``, ``email``, ``company``).
        """
        return self._post("datachoices/productupdate/submit",
                          json_data=form_data)
