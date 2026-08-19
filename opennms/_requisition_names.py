"""Requisition Names REST API – /rest/requisitionNames."""


class RequisitionNamesMixin:
    def get_requisition_names(self):
        """List all requisition (foreign source) names."""
        return self._get("requisitionNames")
