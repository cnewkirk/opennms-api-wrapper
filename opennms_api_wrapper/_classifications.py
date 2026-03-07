"""Flow Classification REST API – /rest/classifications."""
from .types import ClassificationRule, ClassificationGroup, ClassifyRequest


class ClassificationsMixin:
    # ------------------------------------------------------------------
    # Rules
    # ------------------------------------------------------------------

    def get_classification_rules(self, limit: int = 10, offset: int = 0):
        """List classification rules.

        Args:
            limit: Maximum number of results.
            offset: Number of results to skip.
        """
        params = {"limit": limit, "offset": offset}
        return self._get("classifications", params=params)

    def get_classification_rule(self, rule_id: int):
        """Get a specific classification rule by *rule_id*."""
        return self._get(f"classifications/{rule_id}")

    def create_classification_rule(self, rule: ClassificationRule):
        """Create a new classification rule.

        Args:
            rule: Rule definition dict. Common keys: ``name``,
                ``dstAddress``, ``dstPort``, ``srcAddress``, ``srcPort``,
                ``protocol``, ``exporterFilter``, ``groupId``.
        """
        return self._post("classifications", json_data=rule)

    def update_classification_rule(self, rule_id: int, rule: ClassificationRule):
        """Update a classification rule.

        Args:
            rule_id: Database ID of the rule to update.
            rule: Updated rule definition dict.
        """
        return self._put(f"classifications/{rule_id}", json_data=rule)

    def delete_classification_rules(self, group_id: int = None):
        """Delete classification rules, optionally filtered by group.

        Args:
            group_id: When provided, delete only rules in this group.
        """
        params = {"groupId": group_id} if group_id is not None else None
        return self._delete("classifications", params=params)

    def delete_classification_rule(self, rule_id: int):
        """Delete a specific classification rule."""
        return self._delete(f"classifications/{rule_id}")

    def classify(self, request: ClassifyRequest):
        """Classify a flow record against the configured rules.

        Args:
            request: Classification request dict with keys such as
                ``srcAddress``, ``srcPort``, ``dstAddress``, ``dstPort``,
                ``protocol``, ``exporterAddress``.
        """
        return self._post("classifications/classify", json_data=request)

    # ------------------------------------------------------------------
    # Groups
    # ------------------------------------------------------------------

    def get_classification_groups(self, limit: int = 10,
                                  offset: int = 0):
        """List classification groups.

        Args:
            limit: Maximum number of results.
            offset: Number of results to skip.
        """
        params = {"limit": limit, "offset": offset}
        return self._get("classifications/groups", params=params)

    def get_classification_group(self, group_id: int):
        """Get a specific classification group by *group_id*."""
        return self._get(f"classifications/groups/{group_id}")

    def create_classification_group(self, group: ClassificationGroup):
        """Create a new classification group.

        Args:
            group: Group definition dict with key ``name``.
        """
        return self._post("classifications/groups", json_data=group)

    def update_classification_group(self, group_id: int, group: ClassificationGroup):
        """Update a classification group.

        Args:
            group_id: Database ID of the group.
            group: Updated group definition dict.
        """
        return self._put(f"classifications/groups/{group_id}",
                         json_data=group)

    def delete_classification_group(self, group_id: int):
        """Delete a classification group."""
        return self._delete(f"classifications/groups/{group_id}")

    def import_classification_rules(self, group_id: int,
                                    csv_text: str):
        """Import classification rules from CSV text into a group.

        Args:
            group_id: Target group database ID.
            csv_text: CSV-formatted rules to import.
        """
        return self._post_text(
            f"classifications/groups/{group_id}",
            data=csv_text,
            content_type="text/comma-separated-values")

    # ------------------------------------------------------------------
    # Protocols
    # ------------------------------------------------------------------

    def get_classification_protocols(self):
        """List all known protocols used by the classification engine."""
        return self._get("classifications/protocols")
