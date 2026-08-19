"""Graph / Topology REST API – /rest/graphs."""
from ._base import _OpenNMSBase
from typing import Optional


class GraphsMixin(_OpenNMSBase):
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
                       vertices_in_focus: Optional[list] = None):
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

    def get_graph_search_results(self, namespace: str, provider_id: Optional[str] = None,
                                 criteria: Optional[str] = None, context: Optional[str] = None):
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
                         params=params)

    # ------------------------------------------------------------------
    # Prefab graphs
    # ------------------------------------------------------------------

    def get_prefab_graph_names(self):
        """List all prefab graph names.

        Hits the same path as ``get_graph_containers()`` but documents the
        expected return type when the server is configured for prefab graphs
        (a list of name strings).
        """
        return self._get("graphs")

    def get_prefab_graph(self, name: str):
        """Get a specific prefab graph definition by *name*."""
        return self._get(f"graphs/{name}")

    def get_prefab_graphs_for_resource(self, resource_id: str):
        """List prefab graphs available for a given *resource_id*.

        Args:
            resource_id: Full resource ID, e.g.
                ``"node[1].interfaceSnmp[eth0-04013f75f101]"``.
        """
        return self._get(f"graphs/for/{resource_id}")

    def get_prefab_graphs_for_node(self, node_criteria: str):
        """List prefab graphs available for a given node.

        Args:
            node_criteria: Node DB ID or ``"foreignSource:foreignId"``.
        """
        return self._get(f"graphs/fornode/{node_criteria}")
