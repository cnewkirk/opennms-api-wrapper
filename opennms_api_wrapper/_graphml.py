"""GraphML REST API – /rest/graphml.

The GraphML endpoint is XML-only by design: GraphML is itself an XML
format, so request and response bodies are raw GraphML documents
rather than JSON.
"""
from ._base import _OpenNMSBase


class GraphMlMixin(_OpenNMSBase):
    def get_graphml(self, graph_name: str) -> str:
        """Get a stored GraphML graph definition.

        Args:
            graph_name: Name of the GraphML graph.

        Returns:
            The GraphML document as an XML string.
        """
        return self._get_text(f"graphml/{graph_name}",
                              accept="application/xml")

    def create_graphml(self, graph_name: str, graphml_xml: str):
        """Create a new GraphML graph.

        The server returns 500 (not 400) when the graph already
        exists or the document fails validation — a valid document
        needs a ``label`` ``<key>`` and per-graph ``<data>`` entries
        (see the OpenNMS GraphML docs).

        Args:
            graph_name: Name to store the graph under.
            graphml_xml: GraphML document as an XML string.
        """
        return self._post_text(f"graphml/{graph_name}", graphml_xml,
                               "application/xml", accept="*/*")

    def delete_graphml(self, graph_name: str):
        """Delete a stored GraphML graph.

        Args:
            graph_name: Name of the GraphML graph.
        """
        return self._delete(f"graphml/{graph_name}", accept="*/*")
