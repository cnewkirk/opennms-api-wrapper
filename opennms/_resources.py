"""Resources REST API – /rest/resources."""
from ._base import _OpenNMSBase
from typing import Optional


class ResourcesMixin(_OpenNMSBase):
    def get_resources(self, depth: int = 1):
        """Return the full resource tree (can be expensive on large systems).

        Args:
            depth: Tree depth limit. ``-1`` for unlimited depth.
        """
        return self._get("resources", params={"depth": depth})

    def get_resource(self, resource_id: str, depth: int = -1):
        """Return the resource tree rooted at *resource_id*.

        *resource_id* examples:
        - ``"node[1]"``
        - ``"node[Servers:router01]"``
        - ``"node[1].interfaceSnmp[eth0-04013f75f101]"``

        Args:
            depth: Tree depth limit. ``-1`` (default) returns single resource.
        """
        return self._get(f"resources/{resource_id}", params={"depth": depth})

    def get_resources_for_node(self, node_criteria: str):
        """Return all resources for a node.

        Args:
            node_criteria: Node DB ID (``"1"``) or ``"foreignSource:foreignId"``.
        """
        return self._get(f"resources/fornode/{node_criteria}")

    def get_resources_select(
        self,
        nodes: Optional[list] = None,
        filter_rules: Optional[list] = None,
        node_subresources: Optional[list] = None,
        string_properties: Optional[list] = None,
    ):
        """Return a partial selection of the resource tree.

        Args:
            nodes: List of node IDs or ``"FS:FID"`` strings.
            filter_rules: List of filter rule strings.
            node_subresources: List of subresource name strings.
            string_properties: List of string property names to include.
        """
        params = {}
        if nodes:
            params["nodes"] = ",".join(str(n) for n in nodes)
        if filter_rules:
            params["filterRules"] = ",".join(filter_rules)
        if node_subresources:
            params["nodeSubresources"] = ",".join(node_subresources)
        if string_properties:
            params["stringProperties"] = ",".join(string_properties)
        return self._get("resources/select", params=params)

    def delete_resource(self, resource_id: str):
        """Delete a resource and all its child resources.

        Args:
            resource_id: Resource ID string (see ``get_resource()``).
        """
        return self._delete(f"resources/{resource_id}")
