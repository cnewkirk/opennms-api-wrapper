"""Graph / Topology REST API – /rest/graphs."""


class GraphsMixin:
    def get_graph_containers(self):
        """List all registered graph containers and their metadata."""
        return self._get("graphs")

    def get_graph_container(self, container_id: str):
        """Get a specific graph container by *container_id*."""
        return self._get(f"graphs/{container_id}")

    def get_graph(self, container_id: str, namespace: str):
        """Get a graph by *namespace* from *container_id*."""
        return self._get(f"graphs/{container_id}/{namespace}")

    def get_graph_view(self, container_id: str, namespace: str,
                       semantic_zoom_level: int = 1,
                       vertices_in_focus: list = None):
        """Get a focused graph view via POST.

        Args:
            container_id: Graph container ID.
            namespace: Graph namespace.
            semantic_zoom_level: SZL (default 1).
            vertices_in_focus: List of vertex ID strings in the form
                ``"namespace:vertex_id"``.
        """
        body = {
            "semanticZoomLevel": semantic_zoom_level,
            "verticesInFocus": vertices_in_focus or [],
        }
        return self._post(f"graphs/{container_id}/{namespace}", json_data=body)

    def get_graph_search_suggestions(self, namespace: str, search_term: str):
        """Return search suggestions for graph elements in *namespace*.

        Args:
            namespace: Graph namespace to search within.
            search_term: Partial string to match against graph element labels.
        """
        return self._get(
            f"graphs/search/suggestions/{namespace}",
            params={"s": search_term},
        )

    def get_graph_search_results(self, namespace: str, provider_id: str = None,
                                 criteria: str = None, context: str = None):
        """Return search results for graph elements in *namespace*.

        Args:
            namespace: Graph namespace to search within.
            provider_id: Optional search provider ID to restrict results.
            criteria: Optional search criteria string.
            context: Optional context string passed to the search provider.
        """
        params = {}
        if provider_id:
            params["providerId"] = provider_id
        if criteria:
            params["criteria"] = criteria
        if context:
            params["context"] = context
        return self._get(f"graphs/search/results/{namespace}",
                         params=params or None)
