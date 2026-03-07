"""Categories REST API – /rest/categories."""


class CategoriesMixin:
    # ==================================================================
    # Categories CRUD
    # ==================================================================

    def get_categories(self):
        """List all configured surveillance categories."""
        return self._get("categories")

    def get_category(self, category: str):
        """Get a specific category by *category* name."""
        return self._get(f"categories/{category}")

    def create_category(self, category: dict):
        """Add a new surveillance category.

        Args:
            category: Category dict. Example:
                ``{"name": "Production", "authorizedGroups": []}``
        """
        return self._post("categories", json_data=category)

    def update_category(self, category: str, data: dict):
        """Update a category.

        Args:
            category: Category name to update.
            data: Dict of category fields to change.
        """
        return self._put(f"categories/{category}", json_data=data)

    def delete_category(self, category: str):
        """Delete a category."""
        return self._delete(f"categories/{category}")

    # ==================================================================
    # Category ↔ Node associations
    # ==================================================================

    def get_node_categories_list(self, node_id):
        """Get all categories for *node_id*."""
        return self._get(f"categories/nodes/{node_id}")

    def get_category_for_node(self, category: str, node_id):
        """Get a specific category for *node_id*."""
        return self._get(f"categories/{category}/nodes/{node_id}")

    def associate_category_with_node(self, category: str, node_id):
        """Associate *category* with *node_id*."""
        return self._put(f"categories/{category}/nodes/{node_id}")

    def dissociate_category_from_node(self, category: str, node_id):
        """Remove *category* from *node_id*."""
        return self._delete(f"categories/{category}/nodes/{node_id}")

    # ==================================================================
    # Category ↔ Group associations
    # ==================================================================

    def get_categories_for_group(self, group: str):
        """Get categories associated with user group *group*."""
        return self._get(f"categories/groups/{group}")

    def associate_category_with_group(self, category: str, group: str):
        """Associate *category* with user group *group*."""
        return self._put(f"categories/{category}/groups/{group}")

    def dissociate_category_from_group(self, category: str, group: str):
        """Remove *category* from user group *group*."""
        return self._delete(f"categories/{category}/groups/{group}")
