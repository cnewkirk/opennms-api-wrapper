"""EnLinkd REST API v2 – /api/v2/enlinkd."""


class EnLinkdMixin:
    def get_node_enlinkd(self, node_criteria):
        """Get all EnLinkd topology data for a node (aggregate).

        Args:
            node_criteria: Node DB ID or ``foreignSource:foreignId``.

        Returns:
            dict with lldpLinkNodes, cdpLinkNodes, ospfLinkNodes,
            isisLinkNodes, bridgeLinkNodes (lists), plus element
            dicts/lists for each protocol.
        """
        return self._get(f"enlinkd/{node_criteria}", v2=True)

    def get_node_lldp_links(self, node_criteria):
        """Get LLDP link topology for a node.

        Args:
            node_criteria: Node DB ID or ``foreignSource:foreignId``.
        """
        return self._get(f"enlinkd/lldp_links/{node_criteria}",
                         v2=True)

    def get_node_cdp_links(self, node_criteria):
        """Get CDP link topology for a node.

        Args:
            node_criteria: Node DB ID or ``foreignSource:foreignId``.
        """
        return self._get(f"enlinkd/cdp_links/{node_criteria}",
                         v2=True)

    def get_node_ospf_links(self, node_criteria):
        """Get OSPF link topology for a node.

        Args:
            node_criteria: Node DB ID or ``foreignSource:foreignId``.
        """
        return self._get(f"enlinkd/ospf_links/{node_criteria}",
                         v2=True)

    def get_node_isis_links(self, node_criteria):
        """Get IS-IS link topology for a node.

        Args:
            node_criteria: Node DB ID or ``foreignSource:foreignId``.
        """
        return self._get(f"enlinkd/isis_links/{node_criteria}",
                         v2=True)

    def get_node_bridge_links(self, node_criteria):
        """Get bridge link topology for a node.

        Args:
            node_criteria: Node DB ID or ``foreignSource:foreignId``.
        """
        return self._get(f"enlinkd/bridge_links/{node_criteria}",
                         v2=True)

    def get_node_lldp_element(self, node_criteria):
        """Get the LLDP element (chassis info) for a node.

        Args:
            node_criteria: Node DB ID or ``foreignSource:foreignId``.
        """
        return self._get(f"enlinkd/lldp_elems/{node_criteria}",
                         v2=True)

    def get_node_cdp_element(self, node_criteria):
        """Get the CDP element (global config) for a node.

        Args:
            node_criteria: Node DB ID or ``foreignSource:foreignId``.
        """
        return self._get(f"enlinkd/cdp_elems/{node_criteria}",
                         v2=True)

    def get_node_ospf_element(self, node_criteria):
        """Get the OSPF element (router info) for a node.

        Args:
            node_criteria: Node DB ID or ``foreignSource:foreignId``.
        """
        return self._get(f"enlinkd/ospf_elems/{node_criteria}",
                         v2=True)

    def get_node_isis_element(self, node_criteria):
        """Get the IS-IS element (system info) for a node.

        Args:
            node_criteria: Node DB ID or ``foreignSource:foreignId``.
        """
        return self._get(f"enlinkd/isis_elems/{node_criteria}",
                         v2=True)

    def get_node_bridge_elements(self, node_criteria):
        """Get bridge elements (one per VLAN) for a node.

        Args:
            node_criteria: Node DB ID or ``foreignSource:foreignId``.
        """
        return self._get(f"enlinkd/bridge_elems/{node_criteria}",
                         v2=True)
