"""Flow REST API – /rest/flows (read-only)."""


class FlowsMixin:
    # ------------------------------------------------------------------
    # Overview
    # ------------------------------------------------------------------

    def get_flow_count(self):
        """Return the number of flows available."""
        return self._get("flows/count")

    # ------------------------------------------------------------------
    # Exporters
    # ------------------------------------------------------------------

    def get_flow_exporters(self):
        """Return basic information for all exporter nodes that have flows."""
        return self._get("flows/exporters")

    def get_flow_exporter(self, node_criteria: str):
        """Return details about a specific flow exporter node.

        Args:
            node_criteria: Node DB ID or ``"foreignSource:foreignId"``.
        """
        return self._get(f"flows/exporters/{node_criteria}")

    # ------------------------------------------------------------------
    # Applications
    # ------------------------------------------------------------------

    def get_flow_applications(self, top_n: int = 10, start: int = -14400000,
                              end: int = 0, if_index: int = None,
                              exporter_node: str = None,
                              include_other: bool = False):
        """Return traffic stats for the top *top_n* applications.

        Args:
            top_n: Number of top applications to return.
            start: Start time in ms since epoch. Negative values are relative
                to *end* (default ``-14400000`` = 4 hours ago).
            end: End time in ms since epoch. ``0`` means now.
            if_index: Optional SNMP ifIndex to filter by interface.
            exporter_node: Optional node criteria (DB ID or
                ``"foreignSource:foreignId"``) to filter by exporter.
            include_other: When ``True`` include an aggregated "Other"
                category for traffic outside the top N.
        """
        params = self._flow_params(start, end, if_index, exporter_node)
        params["N"] = top_n
        params["includeOther"] = str(include_other).lower()
        return self._get("flows/applications", params=params)

    def get_flow_applications_enumerate(self, start: int = -14400000,
                                        end: int = 0, if_index: int = None,
                                        exporter_node: str = None,
                                        limit: int = 10):
        """List application names that have flows in the given time range.

        Args:
            start: Start time in ms since epoch. Negative values are relative
                to *end* (default ``-14400000`` = 4 hours ago).
            end: End time in ms since epoch. ``0`` means now.
            if_index: Optional SNMP ifIndex to filter by interface.
            exporter_node: Optional node criteria to filter by exporter.
            limit: Max number of results to return. Use ``0`` for all.
        """
        params = self._flow_params(start, end, if_index, exporter_node)
        params["limit"] = limit
        return self._get("flows/applications/enumerate", params=params)

    def get_flow_applications_series(self, top_n: int = 10,
                                     start: int = -14400000, end: int = 0,
                                     step: int = 300000,
                                     if_index: int = None,
                                     exporter_node: str = None,
                                     include_other: bool = False):
        """Return time-series data for the top *top_n* applications.

        Args:
            top_n: Number of top applications to return.
            start: Start time in ms since epoch. Negative values are relative
                to *end* (default ``-14400000`` = 4 hours ago).
            end: End time in ms since epoch. ``0`` means now.
            step: Requested interval between data points in ms (default 5 min).
            if_index: Optional SNMP ifIndex to filter by interface.
            exporter_node: Optional node criteria to filter by exporter.
            include_other: When ``True`` include an aggregated "Other" series.
        """
        params = self._flow_params(start, end, if_index, exporter_node)
        params.update({"N": top_n, "step": step,
                        "includeOther": str(include_other).lower()})
        return self._get("flows/applications/series", params=params)

    # ------------------------------------------------------------------
    # Conversations
    # ------------------------------------------------------------------

    def get_flow_conversations(self, top_n: int = 10, start: int = -14400000,
                               end: int = 0, if_index: int = None,
                               exporter_node: str = None,
                               include_other: bool = False):
        """Return traffic stats for the top *top_n* conversations.

        Args:
            top_n: Number of top conversations to return.
            start: Start time in ms since epoch. Negative values are relative
                to *end* (default ``-14400000`` = 4 hours ago).
            end: End time in ms since epoch. ``0`` means now.
            if_index: Optional SNMP ifIndex to filter by interface.
            exporter_node: Optional node criteria to filter by exporter.
            include_other: When ``True`` include an aggregated "Other" category.
        """
        params = self._flow_params(start, end, if_index, exporter_node)
        params.update({"N": top_n,
                        "includeOther": str(include_other).lower()})
        return self._get("flows/conversations", params=params)

    def get_flow_conversations_enumerate(self, start: int = -14400000,
                                         end: int = 0, if_index: int = None,
                                         exporter_node: str = None,
                                         limit: int = 10):
        """List conversations that have flows in the given time range.

        Args:
            start: Start time in ms since epoch. Negative values are relative
                to *end* (default ``-14400000`` = 4 hours ago).
            end: End time in ms since epoch. ``0`` means now.
            if_index: Optional SNMP ifIndex to filter by interface.
            exporter_node: Optional node criteria to filter by exporter.
            limit: Max number of results to return. Use ``0`` for all.
        """
        params = self._flow_params(start, end, if_index, exporter_node)
        params["limit"] = limit
        return self._get("flows/conversations/enumerate", params=params)

    def get_flow_conversations_series(self, top_n: int = 10,
                                      start: int = -14400000, end: int = 0,
                                      step: int = 300000,
                                      if_index: int = None,
                                      exporter_node: str = None,
                                      include_other: bool = False):
        """Return time-series data for the top *top_n* conversations.

        Args:
            top_n: Number of top conversations to return.
            start: Start time in ms since epoch. Negative values are relative
                to *end* (default ``-14400000`` = 4 hours ago).
            end: End time in ms since epoch. ``0`` means now.
            step: Requested interval between data points in ms (default 5 min).
            if_index: Optional SNMP ifIndex to filter by interface.
            exporter_node: Optional node criteria to filter by exporter.
            include_other: When ``True`` include an aggregated "Other" series.
        """
        params = self._flow_params(start, end, if_index, exporter_node)
        params.update({"N": top_n, "step": step,
                        "includeOther": str(include_other).lower()})
        return self._get("flows/conversations/series", params=params)

    # ------------------------------------------------------------------
    # Hosts
    # ------------------------------------------------------------------

    def get_flow_hosts(self, top_n: int = 10, start: int = -14400000,
                       end: int = 0, if_index: int = None,
                       exporter_node: str = None,
                       include_other: bool = False):
        """Return traffic stats for the top *top_n* hosts.

        Args:
            top_n: Number of top hosts to return.
            start: Start time in ms since epoch. Negative values are relative
                to *end* (default ``-14400000`` = 4 hours ago).
            end: End time in ms since epoch. ``0`` means now.
            if_index: Optional SNMP ifIndex to filter by interface.
            exporter_node: Optional node criteria to filter by exporter.
            include_other: When ``True`` include an aggregated "Other" category.
        """
        params = self._flow_params(start, end, if_index, exporter_node)
        params.update({"N": top_n,
                        "includeOther": str(include_other).lower()})
        return self._get("flows/hosts", params=params)

    def get_flow_hosts_enumerate(self, start: int = -14400000, end: int = 0,
                                 if_index: int = None,
                                 exporter_node: str = None, limit: int = 10):
        """List hosts that have flows in the given time range.

        Args:
            start: Start time in ms since epoch. Negative values are relative
                to *end* (default ``-14400000`` = 4 hours ago).
            end: End time in ms since epoch. ``0`` means now.
            if_index: Optional SNMP ifIndex to filter by interface.
            exporter_node: Optional node criteria to filter by exporter.
            limit: Max number of results to return. Use ``0`` for all.
        """
        params = self._flow_params(start, end, if_index, exporter_node)
        params["limit"] = limit
        return self._get("flows/hosts/enumerate", params=params)

    def get_flow_hosts_series(self, top_n: int = 10, start: int = -14400000,
                              end: int = 0, step: int = 300000,
                              if_index: int = None, exporter_node: str = None,
                              include_other: bool = False):
        """Return time-series data for the top *top_n* hosts.

        Args:
            top_n: Number of top hosts to return.
            start: Start time in ms since epoch. Negative values are relative
                to *end* (default ``-14400000`` = 4 hours ago).
            end: End time in ms since epoch. ``0`` means now.
            step: Requested interval between data points in ms (default 5 min).
            if_index: Optional SNMP ifIndex to filter by interface.
            exporter_node: Optional node criteria to filter by exporter.
            include_other: When ``True`` include an aggregated "Other" series.
        """
        params = self._flow_params(start, end, if_index, exporter_node)
        params.update({"N": top_n, "step": step,
                        "includeOther": str(include_other).lower()})
        return self._get("flows/hosts/series", params=params)

    # ------------------------------------------------------------------
    # DSCP
    # ------------------------------------------------------------------

    def get_flow_dscp(self, top_n: int = 10, start: int = -14400000,
                      end: int = 0, if_index: int = None,
                      exporter_node: str = None,
                      include_other: bool = False):
        """Return traffic stats for the top *top_n* DSCP values.

        Args:
            top_n: Number of top DSCP values to return.
            start: Start time in ms since epoch (negative = relative to *end*).
            end: End time in ms since epoch. ``0`` means now.
            if_index: Optional SNMP ifIndex to filter by interface.
            exporter_node: Optional node criteria to filter by exporter.
            include_other: When ``True`` include an aggregated "Other" category.
        """
        params = self._flow_params(start, end, if_index, exporter_node)
        params.update({"N": top_n,
                        "includeOther": str(include_other).lower()})
        return self._get("flows/dscp", params=params)

    def get_flow_dscp_enumerate(self, start: int = -14400000, end: int = 0,
                                if_index: int = None,
                                exporter_node: str = None,
                                limit: int = 10):
        """List DSCP values that have flows in the given time range.

        Args:
            start: Start time in ms since epoch (negative = relative to *end*).
            end: End time in ms since epoch. ``0`` means now.
            if_index: Optional SNMP ifIndex to filter by interface.
            exporter_node: Optional node criteria to filter by exporter.
            limit: Max number of results to return. Use ``0`` for all.
        """
        params = self._flow_params(start, end, if_index, exporter_node)
        params["limit"] = limit
        return self._get("flows/dscp/enumerate", params=params)

    def get_flow_dscp_series(self, top_n: int = 10, start: int = -14400000,
                             end: int = 0, step: int = 300000,
                             if_index: int = None,
                             exporter_node: str = None,
                             include_other: bool = False):
        """Return time-series data for the top *top_n* DSCP values.

        Args:
            top_n: Number of top DSCP values to return.
            start: Start time in ms since epoch (negative = relative to *end*).
            end: End time in ms since epoch. ``0`` means now.
            step: Interval between data points in ms (default 5 min).
            if_index: Optional SNMP ifIndex to filter by interface.
            exporter_node: Optional node criteria to filter by exporter.
            include_other: When ``True`` include an aggregated "Other" series.
        """
        params = self._flow_params(start, end, if_index, exporter_node)
        params.update({"N": top_n, "step": step,
                        "includeOther": str(include_other).lower()})
        return self._get("flows/dscp/series", params=params)

    # ------------------------------------------------------------------
    # Flow graph URL
    # ------------------------------------------------------------------

    def get_flow_graph_url(self):
        """Return the configured flow graph URL."""
        return self._get("flows/flowGraphUrl")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _flow_params(start: int, end: int, if_index, exporter_node) -> dict:
        """Build the common query parameter dict shared by all flow API methods."""
        params: dict = {"start": start, "end": end}
        if if_index is not None:
            params["ifIndex"] = if_index
        if exporter_node is not None:
            params["exporterNode"] = exporter_node
        return params
