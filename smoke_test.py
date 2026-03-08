#!/usr/bin/env python3
"""
smoke_test.py – Exercise the OpenNMS API wrapper against a live server.

Read-only mode (default) is safe to run against any server, including
production.  It issues only GET requests and makes no changes.

Write mode (--write) creates and deletes objects on the server.  It will
prompt for explicit confirmation before running.  Only use write mode against
a dev or staging instance — never against production.

Environment variables:
    OPENNMS_URL         Base URL, e.g. "https://opennms.example.com:8443"  (required)
    OPENNMS_USER        OpenNMS username (needs at minimum the ``rest`` role)  (required)
    OPENNMS_PASSWORD    Password  (required)
    OPENNMS_VERIFY_SSL  Set to "false" to disable SSL verification (default: true)
    OPENNMS_TIMEOUT     Request timeout in seconds (default: 60)

Usage:
    python smoke_test.py                 # read-only — safe for any server
    python smoke_test.py --write         # write ops — prompts for confirmation
    python smoke_test.py --write --yes   # write ops — skip prompt (CI only)
    python smoke_test.py --no-color      # plain output for log files
    python smoke_test.py --skip get_resources,get_flow  # skip slow tests
"""

import argparse
import os
import re
import sys
import time

import opennms_api_wrapper as opennms


# ── Output ─────────────────────────────────────────────────────────────────────

_passed = _failed = _skipped = _warned = 0
_failures: list = []
_warnings: list = []
_skip_prefixes: list = []

# Sentinel returned by run() when the underlying call raised an exception.
# Distinguishes "call failed" from "call succeeded and returned None (204)".
_FAILED = object()


def _section(title: str):
    print(f"\n[{title}]")


def _ok(label: str, detail: str = ""):
    global _passed
    _passed += 1
    suffix = f"  \033[2m{detail}\033[0m" if detail else ""
    print(f"  \033[32mPASS\033[0m  {label}{suffix}")


def _fail(label: str, err):
    global _failed
    _failed += 1
    _failures.append((label, str(err)))
    print(f"  \033[31mFAIL\033[0m  {label}  \033[2m{err}\033[0m")


def _skip(label: str, reason: str = ""):
    global _skipped
    _skipped += 1
    suffix = f"  ({reason})" if reason else ""
    print(f"  \033[33mSKIP\033[0m  {label}{suffix}")


def _warn_msg(label: str, err, note: str = None):
    global _warned
    _warned += 1
    suffix = f"  ({note})" if note else ""
    _warnings.append((label, f"{err}{suffix}"))
    print(f"  \033[33mWARN\033[0m  {label}  \033[2m{err}{suffix}\033[0m")


def _should_skip(label: str) -> bool:
    """Return True if *label* matches any --skip prefix."""
    return any(label.startswith(p) for p in _skip_prefixes)


def run(label: str, fn, *args, detail_fn=None, **kwargs):
    """Call *fn* and record PASS or FAIL.

    Returns the call's return value, or ``_FAILED`` if an exception was raised.
    """
    if _should_skip(label):
        _skip(label, "--skip")
        return _FAILED
    try:
        result = fn(*args, **kwargs)
        detail = ""
        if detail_fn is not None and result is not None:
            try:
                detail = str(detail_fn(result))
            except Exception:
                pass
        _ok(label, detail)
        return result
    except Exception as exc:
        _fail(label, exc)
        return _FAILED


def warn(label: str, fn, *args, note: str = None, detail_fn=None, **kwargs):
    """Like run(), but records WARN instead of FAIL on error.

    Args:
        note: Optional context appended to warning output (e.g. plugin
            dependency).
    """
    if _should_skip(label):
        _skip(label, "--skip")
        return _FAILED
    try:
        result = fn(*args, **kwargs)
        detail = ""
        if detail_fn is not None and result is not None:
            try:
                detail = str(detail_fn(result))
            except Exception:
                pass
        _ok(label, detail)
        return result
    except Exception as exc:
        _warn_msg(label, exc, note)
        return _FAILED


# ── Data helpers ───────────────────────────────────────────────────────────────

def _n(result, list_key: str = None) -> str:
    """Return a short item-count summary for the detail column."""
    if result is None:
        return ""
    if isinstance(result, int):
        return str(result)
    if isinstance(result, list):
        return f"{len(result)} items"
    if isinstance(result, dict):
        if list_key and list_key in result:
            items = result[list_key]
            return f"{len(items) if isinstance(items, list) else items} items"
        return "ok"
    return "ok"


def _first(collection_fn, list_key: str, id_key: str = "id", **extra):
    """Call *collection_fn(limit=1)* and return *(first_item, first_id)*.

    Returns *(None, None)* on error or empty result.
    """
    try:
        result = collection_fn(limit=1, **extra)
        items = []
        if isinstance(result, dict):
            items = result.get(list_key, [])
        elif isinstance(result, list):
            items = result
        if items:
            return items[0], items[0].get(id_key)
    except Exception:
        pass
    return None, None


# ── Read-only tests ────────────────────────────────────────────────────────────

def test_info(c):
    _section("info")
    run("get_info", c.get_info,
        detail_fn=lambda r: r.get("displayVersion", r.get("version", ""))
                            if isinstance(r, dict) else "")


def test_alarms(c):
    _section("alarms")
    run("get_alarms",              c.get_alarms, limit=5,
        detail_fn=lambda r: _n(r, "alarm"))
    warn("get_alarm_count",        c.get_alarm_count,
         detail_fn=lambda r: str(r))
    run("get_alarm_stats",         c.get_alarm_stats)
    run("get_alarm_stats_by_severity", c.get_alarm_stats_by_severity)
    warn("get_alarm_history",      c.get_alarm_history,
         note="requires opennms-alarm-history-elastic Karaf feature")
    run("get_alarms_v2",           c.get_alarms_v2, limit=5,
        detail_fn=lambda r: _n(r, "alarm"))

    _, aid = _first(c.get_alarms, "alarm")
    if aid:
        run(f"get_alarm                id={aid}", c.get_alarm, aid,
            detail_fn=lambda r: r.get("severity", "") if isinstance(r, dict) else "")
        run(f"get_alarm_v2             id={aid}", c.get_alarm_v2, aid)
        warn(f"get_alarm_history_at     id={aid}", c.get_alarm_history_at, aid,
             note="requires opennms-alarm-history-elastic Karaf feature")
        warn(f"get_alarm_history_states id={aid}", c.get_alarm_history_states, aid,
             note="requires opennms-alarm-history-elastic Karaf feature")
    else:
        for lbl in ("get_alarm", "get_alarm_v2",
                    "get_alarm_history_at", "get_alarm_history_states"):
            _skip(lbl, "no alarms")


def test_events(c):
    _section("events")
    # Unfiltered event queries can time out on large systems (33M+ rows).
    # Filter by the lowest-ID node (typically the self-monitor) to hit an
    # indexed column and avoid full table scans.
    _, nid = _first(c.get_nodes, "node", order_by="id", order="asc")
    node_filter = {"node.id": nid} if nid else {}
    result = run("get_events", c.get_events, limit=5, **node_filter,
                 detail_fn=lambda r: _n(r, "event"))
    warn("get_event_count", c.get_event_count, detail_fn=lambda r: str(r))

    eid = None
    if isinstance(result, dict):
        events = result.get("event", [])
        if events:
            eid = events[0].get("id")
    if eid:
        run(f"get_event  id={eid}", c.get_event, eid)
    else:
        _skip("get_event", "no events")


def test_acks(c):
    _section("acknowledgements")
    run("get_acks",      c.get_acks, limit=5,
        detail_fn=lambda r: _n(r, "ack"))
    warn("get_ack_count", c.get_ack_count, detail_fn=lambda r: str(r))

    _, ack_id = _first(c.get_acks, "ack")
    if ack_id:
        run(f"get_ack  id={ack_id}", c.get_ack, ack_id)
    else:
        _skip("get_ack", "no acks")


def test_notifications(c):
    _section("notifications")
    run("get_notifications",      c.get_notifications, limit=5,
        detail_fn=lambda r: _n(r, "notification"))
    warn("get_notification_count", c.get_notification_count,
         detail_fn=lambda r: str(r))

    _, nid = _first(c.get_notifications, "notification")
    if nid:
        run(f"get_notification  id={nid}", c.get_notification, nid)
    else:
        _skip("get_notification", "no notifications")


def test_nodes(c):
    _section("nodes")
    run("get_nodes",      c.get_nodes, limit=5, detail_fn=lambda r: _n(r, "node"))
    run("get_node_count",  c.get_node_count, detail_fn=lambda r: str(r))

    _, nid = _first(c.get_nodes, "node")
    if nid:
        run(f"get_node                    id={nid}", c.get_node, nid,
            detail_fn=lambda r: r.get("label", "") if isinstance(r, dict) else "")
        ifaces_r = run(f"get_node_ip_interfaces      id={nid}", c.get_node_ip_interfaces,
            nid, limit=3, detail_fn=lambda r: _n(r, "ipInterface"))
        _ip = None
        _svc = None
        if isinstance(ifaces_r, dict):
            _ifaces = ifaces_r.get("ipInterface", [])
            if _ifaces:
                _ip = _ifaces[0].get("ipAddress")
                if _ip:
                    run(f"get_node_ip_interface       ip={_ip}",
                        c.get_node_ip_interface, nid, _ip)
                    svc_r = run(f"get_node_ip_services        ip={_ip}",
                                c.get_node_ip_services, nid, _ip)
                    if isinstance(svc_r, dict):
                        _svcs = svc_r.get("service", [])
                        if _svcs:
                            _svc = _svcs[0].get("serviceType", {}).get("name")
                            if _svc:
                                run(f"get_node_ip_service     svc={_svc}",
                                    c.get_node_ip_service, nid, _ip, _svc)
        snmp_r = run(f"get_node_snmp_interfaces    id={nid}", c.get_node_snmp_interfaces,
            nid, limit=3, detail_fn=lambda r: _n(r, "snmpInterface"))
        if isinstance(snmp_r, dict):
            _snmps = snmp_r.get("snmpInterface", [])
            if _snmps:
                _ifindex = _snmps[0].get("ifIndex")
                if _ifindex is not None:
                    run(f"get_node_snmp_interface  ifIndex={_ifindex}",
                        c.get_node_snmp_interface, nid, _ifindex)
        cats_r = run(f"get_node_categories         id={nid}", c.get_node_categories, nid)
        if isinstance(cats_r, dict):
            _cats = cats_r.get("category", [])
            if _cats:
                _cname = _cats[0].get("name")
                if _cname:
                    run(f"get_node_category       ({_cname})",
                        c.get_node_category, nid, _cname)
        run(f"get_node_asset_record       id={nid}", c.get_node_asset_record, nid)
        warn(f"get_node_hardware_inventory id={nid}", c.get_node_hardware_inventory, nid,
             note="requires opennms-plugin-provisioning-snmp-hardware-inventory")
        run(f"get_node_metadata           id={nid}", c.get_node_metadata, nid)
        if _ip:
            warn(f"get_interface_metadata    ip={_ip}",
                 c.get_interface_metadata, nid, _ip,
                 note="may 404 if no metadata on interface")
            if _svc:
                warn(f"get_service_metadata     svc={_svc}",
                     c.get_service_metadata, nid, _ip, _svc,
                     note="may 404 if no metadata on service")
        run(f"get_node_outages            id={nid}", c.get_node_outages, nid)
        warn(f"get_resources_for_node      id={nid}", c.get_resources_for_node, str(nid))
    else:
        for lbl in ("get_node", "get_node_ip_interfaces", "get_node_ip_interface",
                    "get_node_ip_services", "get_node_snmp_interfaces",
                    "get_node_snmp_interface", "get_node_categories",
                    "get_node_category", "get_node_asset_record",
                    "get_node_hardware_inventory", "get_node_metadata",
                    "get_interface_metadata", "get_node_outages",
                    "get_resources_for_node"):
            _skip(lbl, "no nodes")


def test_outages(c):
    _section("outages")
    run("get_outages",      c.get_outages, limit=5,
        detail_fn=lambda r: _n(r, "outage"))
    warn("get_outage_count", c.get_outage_count, detail_fn=lambda r: str(r))

    _, oid = _first(c.get_outages, "outage")
    if oid:
        run(f"get_outage  id={oid}", c.get_outage, oid)
    else:
        _skip("get_outage", "no outages")


def test_requisitions(c):
    _section("requisitions")
    result = run("get_requisitions",               c.get_requisitions,
                 detail_fn=lambda r: _n(r, "model-import"))
    warn("get_requisition_count",         c.get_requisition_count,
         detail_fn=lambda r: str(r))
    run("get_deployed_requisitions",      c.get_deployed_requisitions,
        detail_fn=lambda r: _n(r, "model-import"))
    warn("get_deployed_requisition_count", c.get_deployed_requisition_count,
         detail_fn=lambda r: str(r))
    reqs = []
    if isinstance(result, dict):
        reqs = result.get("model-import", result.get("requisition", []))
    elif isinstance(result, list):
        reqs = result
    if reqs and isinstance(reqs, list):
        rname = reqs[0].get("foreign-source") or reqs[0].get("name")
        if rname:
            run(f"get_requisition       ({rname})", c.get_requisition, rname)
            nodes_r = run(f"get_requisition_nodes ({rname})",
                          c.get_requisition_nodes, rname)
            _rnodes = []
            if isinstance(nodes_r, dict):
                _rnodes = nodes_r.get("node", [])
            elif isinstance(nodes_r, list):
                _rnodes = nodes_r
            if _rnodes:
                fid = _rnodes[0].get("foreign-id")
                if fid:
                    run(f"get_requisition_node            ({fid})",
                        c.get_requisition_node, rname, fid)
                    run(f"get_requisition_node_interfaces ({fid})",
                        c.get_requisition_node_interfaces, rname, fid)
                    run(f"get_requisition_node_categories ({fid})",
                        c.get_requisition_node_categories, rname, fid)
                    run(f"get_requisition_node_assets     ({fid})",
                        c.get_requisition_node_assets, rname, fid)
    else:
        _skip("get_requisition / get_requisition_nodes", "no requisitions")


def test_foreign_sources(c):
    _section("foreign sources")
    result = run("get_foreign_sources",              c.get_foreign_sources)
    run("get_deployed_foreign_sources",     c.get_deployed_foreign_sources)
    warn("get_deployed_foreign_source_count", c.get_deployed_foreign_source_count,
         detail_fn=lambda r: str(r))
    run("get_default_foreign_source",       c.get_default_foreign_source)
    sources = []
    if isinstance(result, dict):
        sources = result.get("foreignSource", [])
    elif isinstance(result, list):
        sources = result
    if sources and isinstance(sources, list):
        sname = sources[0].get("name")
        if sname:
            run(f"get_foreign_source           ({sname})", c.get_foreign_source, sname)
            det_r = run(f"get_foreign_source_detectors ({sname})",
                        c.get_foreign_source_detectors, sname)
            dets = det_r if isinstance(det_r, list) else (
                det_r.get("detector", []) if isinstance(det_r, dict) else [])
            if dets:
                dname = dets[0].get("name")
                if dname:
                    run(f"get_foreign_source_detector  ({dname})",
                        c.get_foreign_source_detector, sname, dname)
            pol_r = run(f"get_foreign_source_policies  ({sname})",
                        c.get_foreign_source_policies, sname)
            pols = pol_r if isinstance(pol_r, list) else (
                pol_r.get("policy", []) if isinstance(pol_r, dict) else [])
            if pols:
                pname = pols[0].get("name")
                if pname:
                    run(f"get_foreign_source_policy    ({pname})",
                        c.get_foreign_source_policy, sname, pname)
    else:
        _skip("get_foreign_source / detectors / policies", "no foreign sources")


def test_snmp_config(c):
    _section("snmp config")
    # 127.0.0.1 may not be explicitly configured; a 404 is expected on clean servers.
    run("get_snmp_config (127.0.0.1)", c.get_snmp_config, "127.0.0.1")


def test_groups(c):
    _section("groups")
    result = run("get_groups", c.get_groups, detail_fn=lambda r: _n(r, "group"))
    groups = []
    if isinstance(result, dict):
        groups = result.get("group", [])
    elif isinstance(result, list):
        groups = result
    if groups:
        name = groups[0].get("name")
        run(f"get_group            ({name})", c.get_group, name)
        run(f"get_group_users      ({name})", c.get_group_users, name)
        run(f"get_group_categories ({name})", c.get_group_categories, name)
    else:
        _skip("get_group / get_group_users / get_group_categories", "no groups")


def test_users(c):
    _section("users")
    result = run("get_users", c.get_users, detail_fn=lambda r: _n(r, "user"))
    users = []
    if isinstance(result, dict):
        users = result.get("user", [])
    elif isinstance(result, list):
        users = result
    if users:
        uname = users[0].get("user-id")
        run(f"get_user  ({uname})", c.get_user, uname)
    else:
        _skip("get_user", "no users")


def test_categories(c):
    _section("categories")
    result = run("get_categories", c.get_categories,
                 detail_fn=lambda r: _n(r, "category"))
    cats = []
    if isinstance(result, dict):
        cats = result.get("category", [])
    elif isinstance(result, list):
        cats = result
    if cats:
        name = cats[0].get("name")
        run(f"get_category  ({name})", c.get_category, name)
    else:
        _skip("get_category", "no categories")


def test_sched_outages(c):
    _section("scheduled outages")
    result = run("get_sched_outages", c.get_sched_outages,
                 detail_fn=lambda r: _n(r, "schedules"))
    schedules = []
    if isinstance(result, dict):
        schedules = result.get("schedules", [])
    elif isinstance(result, list):
        schedules = result
    if schedules:
        name = schedules[0].get("name")
        run(f"get_sched_outage  ({name})", c.get_sched_outage, name)
    else:
        _skip("get_sched_outage", "no scheduled outages")


def test_ksc_reports(c):
    _section("ksc reports")
    result = run("get_ksc_reports", c.get_ksc_reports,
                 detail_fn=lambda r: _n(r, "kscReport"))
    warn("get_ksc_report_count", c.get_ksc_report_count,
         detail_fn=lambda r: str(r))
    reports = result.get("kscReport", []) if isinstance(result, dict) else []
    if reports:
        rid = reports[0].get("id")
        run(f"get_ksc_report  id={rid}", c.get_ksc_report, rid)
    else:
        _skip("get_ksc_report", "no KSC reports")


def test_resources(c):
    _section("resources")
    warn("get_resources", c.get_resources, depth=1)


def test_measurements(c):
    _section("measurements")
    # Measurements require a node with collected SNMP performance data.
    # Skip gracefully if no suitable resources can be found.
    try:
        nr = c.get_nodes(limit=1)
        nodes = nr.get("node", []) if isinstance(nr, dict) else []
    except Exception:
        nodes = []
    if not nodes:
        _skip("get_measurements", "no nodes")
        return
    nid = nodes[0].get("id")
    try:
        rr = c.get_resources_for_node(str(nid))
        node_res = rr.get("resource", {}) if isinstance(rr, dict) else {}
        children = (node_res.get("children") or {}).get("resource", [])
        if not isinstance(children, list):
            children = []
        iface_res = next(
            (r for r in children if "interfaceSnmp" in r.get("id", "")),
            None,
        )
    except Exception:
        iface_res = None
    if iface_res is None:
        _skip("get_measurements", "no SNMP interface resources on first node")
        return
    rid = iface_res.get("id", "")
    run("get_measurements  ifInOctets", c.get_measurements, rid, "ifInOctets")


def test_heatmap(c):
    _section("heatmap")
    run("get_heatmap_outages_categories",         c.get_heatmap_outages_categories)
    run("get_heatmap_outages_foreign_sources",    c.get_heatmap_outages_foreign_sources)
    run("get_heatmap_outages_monitored_services", c.get_heatmap_outages_monitored_services)
    run("get_heatmap_alarms_categories",          c.get_heatmap_alarms_categories)
    run("get_heatmap_alarms_foreign_sources",     c.get_heatmap_alarms_foreign_sources)
    run("get_heatmap_alarms_monitored_services",  c.get_heatmap_alarms_monitored_services)
    # nodes_by methods require a grouping key; discover one from categories
    try:
        _cats = c.get_categories()
        cat_name = (_cats.get("category") or [{}])[0].get("name") if isinstance(_cats, dict) else None
    except Exception:
        cat_name = None
    if cat_name:
        run(f"get_heatmap_outages_nodes_by_category ({cat_name})",
            c.get_heatmap_outages_nodes_by_category, cat_name)
        run(f"get_heatmap_alarms_nodes_by_category  ({cat_name})",
            c.get_heatmap_alarms_nodes_by_category, cat_name)
    else:
        _skip("heatmap nodes_by_category", "no categories")
    try:
        _fss = c.get_foreign_sources()
        fs_name = (_fss.get("foreignSource") or [{}])[0].get("name") if isinstance(_fss, dict) else None
    except Exception:
        fs_name = None
    if fs_name:
        run(f"get_heatmap_outages_nodes_by_foreign_source ({fs_name})",
            c.get_heatmap_outages_nodes_by_foreign_source, fs_name)
        run(f"get_heatmap_alarms_nodes_by_foreign_source  ({fs_name})",
            c.get_heatmap_alarms_nodes_by_foreign_source, fs_name)
    else:
        _skip("heatmap nodes_by_foreign_source", "no foreign sources")


def test_maps(c):
    _section("maps")
    result = warn("get_maps", c.get_maps,
                  note="SVG maps may not be available in all versions",
                  detail_fn=lambda r: _n(r, "map"))
    maps = []
    if isinstance(result, dict):
        maps = result.get("map", [])
    elif isinstance(result, list):
        maps = result
    if maps:
        mid = maps[0].get("id")
        run(f"get_map          id={mid}", c.get_map, mid)
        run(f"get_map_elements id={mid}", c.get_map_elements, mid)
    else:
        _skip("get_map / get_map_elements", "no maps")


def test_graphs(c):
    _section("topology graphs")
    result = run("get_graph_containers", c.get_graph_containers)
    containers = []
    if isinstance(result, dict):
        # Response key varies by OpenNMS version
        containers = result.get("graphContainers",
                    result.get("container", []))
    elif isinstance(result, list):
        containers = result
    if containers:
        cid = containers[0].get("id")
        run(f"get_graph_container  ({cid})", c.get_graph_container, cid)
        graphs = containers[0].get("graphs", [])
        if graphs:
            ns = graphs[0].get("namespace")
            run(f"get_graph  ({cid}/{ns})", c.get_graph, cid, ns)
        else:
            _skip("get_graph", "container has no graphs")
    else:
        _skip("get_graph_container / get_graph", "no graph containers")


def test_flows(c):
    _section("flows")
    _flow_note = "requires flow persistence (Elasticsearch/OpenSearch)"
    warn("get_flow_count",    c.get_flow_count,
         note=_flow_note, detail_fn=lambda r: str(r))
    run("get_flow_exporters", c.get_flow_exporters,
        detail_fn=lambda r: _n(r, "exporters"))
    warn("get_flow_applications",           c.get_flow_applications,
         top_n=5, note=_flow_note)
    warn("get_flow_applications_enumerate", c.get_flow_applications_enumerate,
         limit=5, note=_flow_note)
    warn("get_flow_conversations",          c.get_flow_conversations,
         top_n=5, note=_flow_note)
    warn("get_flow_conversations_enumerate",c.get_flow_conversations_enumerate,
         limit=5, note=_flow_note)
    warn("get_flow_hosts",                  c.get_flow_hosts,
         top_n=5, note=_flow_note)
    warn("get_flow_hosts_enumerate",        c.get_flow_hosts_enumerate,
         limit=5, note=_flow_note)


def test_device_config(c):
    _section("device config")
    run("get_device_configs",        c.get_device_configs, limit=5,
        detail_fn=lambda r: _n(r, "deviceConfig"))
    run("get_latest_device_configs", c.get_latest_device_configs, limit=5,
        detail_fn=lambda r: _n(r, "deviceConfig"))


def test_situations(c):
    _section("situations (v2)")
    warn("get_situations", c.get_situations, limit=5,
         note="requires Alarmd situation correlation",
         detail_fn=lambda r: _n(r, "alarm"))


def test_business_services(c):
    _section("business services (v2)")
    result = run("get_business_services", c.get_business_services,
                 detail_fn=lambda r: _n(r, "business-service"))
    bsvcs = []
    if isinstance(result, dict):
        bsvcs = result.get("business-service",
                result.get("business-services", []))
    elif isinstance(result, list):
        bsvcs = result
    if bsvcs:
        bid = bsvcs[0].get("id")
        if bid:
            run(f"get_business_service  id={bid}",
                c.get_business_service, bid)
    else:
        _skip("get_business_service", "no business services")


def test_enlinkd(c):
    _section("enlinkd (v2)")
    _, nid = _first(c.get_nodes, "node")
    _enlinkd_note = "requires enlinkd daemon"
    if nid:
        warn(f"get_node_enlinkd         id={nid}", c.get_node_enlinkd, nid,
             note=_enlinkd_note)
        warn(f"get_node_lldp_links      id={nid}", c.get_node_lldp_links, nid,
             note=_enlinkd_note)
        warn(f"get_node_cdp_links       id={nid}", c.get_node_cdp_links, nid,
             note=_enlinkd_note)
        warn(f"get_node_ospf_links      id={nid}", c.get_node_ospf_links, nid,
             note=_enlinkd_note)
        warn(f"get_node_isis_links      id={nid}", c.get_node_isis_links, nid,
             note=_enlinkd_note)
        warn(f"get_node_bridge_links    id={nid}", c.get_node_bridge_links, nid,
             note=_enlinkd_note)
        warn(f"get_node_lldp_element    id={nid}", c.get_node_lldp_element, nid,
             note=_enlinkd_note)
        warn(f"get_node_cdp_element     id={nid}", c.get_node_cdp_element, nid,
             note=_enlinkd_note)
        warn(f"get_node_ospf_element    id={nid}", c.get_node_ospf_element, nid,
             note=_enlinkd_note)
        warn(f"get_node_isis_element    id={nid}", c.get_node_isis_element, nid,
             note=_enlinkd_note)
        warn(f"get_node_bridge_elements id={nid}", c.get_node_bridge_elements, nid,
             note=_enlinkd_note)
    else:
        _skip("get_node_enlinkd", "no nodes")


def test_v2_interfaces(c):
    _section("ip/snmp interfaces (v2)")
    run("get_ip_interfaces",   c.get_ip_interfaces, limit=5,
        detail_fn=lambda r: _n(r, "ipInterface"))
    run("get_snmp_interfaces", c.get_snmp_interfaces, limit=5,
        detail_fn=lambda r: _n(r, "snmpInterface"))


def test_monitoring_locations(c):
    _section("monitoring locations")
    run("get_monitoring_locations", c.get_monitoring_locations,
        detail_fn=lambda r: _n(r, "location"))
    run("get_monitoring_location_count", c.get_monitoring_location_count,
        detail_fn=lambda r: str(r))
    run("get_default_monitoring_location", c.get_default_monitoring_location)


def test_minions(c):
    _section("minions")
    run("get_minions", c.get_minions,
        detail_fn=lambda r: _n(r, "minion"))
    run("get_minion_count", c.get_minion_count,
        detail_fn=lambda r: str(r))


def test_ifservices(c):
    _section("ifservices")
    run("get_ifservices", c.get_ifservices,
        detail_fn=lambda r: _n(r, "service"))
    run("get_ifservices_v2", c.get_ifservices_v2, limit=5,
        detail_fn=lambda r: _n(r, "service"))


def test_availability(c):
    _section("availability")
    run("get_availability", c.get_availability)
    _, nid = _first(c.get_nodes, "node")
    if nid:
        run(f"get_availability_node  id={nid}", c.get_availability_node, nid)
    else:
        _skip("get_availability_node", "no nodes")


def test_health(c):
    _section("health")
    run("get_health", c.get_health)
    warn("get_health_probe", c.get_health_probe,
         note="returns 599 if any health check is unhealthy")


def test_whoami(c):
    _section("whoami")
    run("get_whoami", c.get_whoami,
        detail_fn=lambda r: r.get("id", "") if isinstance(r, dict) else "")


def test_monitoring_systems(c):
    _section("monitoring systems")
    warn("get_monitoring_system", c.get_monitoring_system,
         note="may not be available on all versions")


def test_prefab_graphs(c):
    _section("prefab graphs")
    run("get_prefab_graph_names", c.get_prefab_graph_names)
    _, nid = _first(c.get_nodes, "node")
    if nid:
        warn(f"get_prefab_graphs_for_node  id={nid}",
             c.get_prefab_graphs_for_node, str(nid),
             note="may time out on large node inventories")
    else:
        _skip("get_prefab_graphs_for_node", "no nodes")


def test_flow_dscp(c):
    _section("flow DSCP")
    _note = "requires flow persistence (Elasticsearch/OpenSearch)"
    warn("get_flow_dscp", c.get_flow_dscp, top_n=5, note=_note)
    warn("get_flow_dscp_enumerate", c.get_flow_dscp_enumerate,
         limit=5, note=_note)
    warn("get_flow_graph_url", c.get_flow_graph_url, note=_note)


def test_business_service_functions(c):
    _section("business service functions (v2)")
    map_r = run("get_map_functions", c.get_map_functions)
    reduce_r = run("get_reduce_functions", c.get_reduce_functions)
    # Extract a function name to test individual lookup
    _mfuncs = map_r if isinstance(map_r, list) else (
        map_r.get("functions", []) if isinstance(map_r, dict) else [])
    if _mfuncs:
        mname = _mfuncs[0] if isinstance(_mfuncs[0], str) else _mfuncs[0].get("name", "")
        if mname:
            run(f"get_map_function  ({mname})", c.get_map_function, mname)
    _rfuncs = reduce_r if isinstance(reduce_r, list) else (
        reduce_r.get("functions", []) if isinstance(reduce_r, dict) else [])
    if _rfuncs:
        rname = _rfuncs[0] if isinstance(_rfuncs[0], str) else _rfuncs[0].get("name", "")
        if rname:
            run(f"get_reduce_function  ({rname})", c.get_reduce_function, rname)


def test_classifications(c):
    _section("classifications")
    _cls_note = "requires flow classification plugin"
    rules_r = warn("get_classification_rules", c.get_classification_rules,
                   note=_cls_note)
    groups_r = warn("get_classification_groups", c.get_classification_groups,
                    note=_cls_note)
    warn("get_classification_protocols", c.get_classification_protocols,
         note=_cls_note)
    # Drill into first rule if available
    rules = []
    if isinstance(rules_r, dict):
        rules = rules_r.get("rule", rules_r.get("classification", []))
    elif isinstance(rules_r, list):
        rules = rules_r
    if rules:
        rid = rules[0].get("id")
        if rid:
            warn(f"get_classification_rule   id={rid}",
                 c.get_classification_rule, rid, note=_cls_note)
    # Drill into first group if available
    groups = []
    if isinstance(groups_r, dict):
        groups = groups_r.get("group", [])
    elif isinstance(groups_r, list):
        groups = groups_r
    if groups:
        gid = groups[0].get("id")
        if gid:
            warn(f"get_classification_group  id={gid}",
                 c.get_classification_group, gid, note=_cls_note)


def test_situation_feedback(c):
    _section("situation feedback")
    warn("get_situation_feedback_tags", c.get_situation_feedback_tags,
         note="requires situation correlation + feedback feature")


def test_user_defined_links(c):
    _section("user-defined links (v2)")
    result = run("get_user_defined_links", c.get_user_defined_links)
    links = []
    if isinstance(result, dict):
        links = result.get("user-defined-link", [])
    elif isinstance(result, list):
        links = result
    if links:
        lid = links[0].get("id")
        if lid:
            run(f"get_user_defined_link  id={lid}",
                c.get_user_defined_link, lid)
    else:
        _skip("get_user_defined_link", "no user-defined links")


def test_applications(c):
    _section("applications (v2)")
    result = run("get_applications", c.get_applications,
                 detail_fn=lambda r: _n(r, "application"))
    apps = []
    if isinstance(result, dict):
        apps = result.get("application", [])
    elif isinstance(result, list):
        apps = result
    if apps:
        aid = apps[0].get("id")
        if aid:
            run(f"get_application  id={aid}", c.get_application, aid)
    else:
        _skip("get_application", "no applications")


def test_perspective_poller(c):
    _section("perspective poller (v2)")
    warn("get_perspective_poller_status (app 1)",
         c.get_perspective_poller_status, 1,
         note="requires perspective poller + application with id=1")


def test_foreign_sources_config(c):
    _section("foreign sources config")
    run("get_foreign_source_config_policies",
        c.get_foreign_source_config_policies)
    run("get_foreign_source_config_detectors",
        c.get_foreign_source_config_detectors)
    run("get_foreign_source_config_assets",
        c.get_foreign_source_config_assets)
    run("get_foreign_source_config_categories",
        c.get_foreign_source_config_categories)


def test_requisition_names(c):
    _section("requisition names")
    run("get_requisition_names", c.get_requisition_names)


def test_snmp_metadata(c):
    _section("snmp metadata (v2)")
    _, nid = _first(c.get_nodes, "node")
    if nid:
        run(f"get_snmp_metadata  id={nid}", c.get_snmp_metadata, nid)
    else:
        _skip("get_snmp_metadata", "no nodes")


def test_provisiond(c):
    _section("provisiond (v2)")
    warn("get_provisiond_status", c.get_provisiond_status,
         note="requires provisiond v2 API support")


def test_eventconf(c):
    _section("eventconf (v2)")
    _ec_note = "requires eventconf v2 API support"
    names_r = warn("get_eventconf_source_names", c.get_eventconf_source_names,
                   note=_ec_note)
    warn("get_eventconf_filter", c.get_eventconf_filter, note=_ec_note)
    warn("get_eventconf_filter_sources", c.get_eventconf_filter_sources,
         note=_ec_note)
    # Drill into first source if source names returned
    src_name = None
    if isinstance(names_r, list) and names_r:
        src_name = names_r[0]
    if src_name:
        warn(f"get_eventconf_source          ({src_name})",
             c.get_eventconf_source, src_name, note=_ec_note)
        warn(f"get_eventconf_filter_events   ({src_name})",
             c.get_eventconf_filter_events, src_name, note=_ec_note)
        warn(f"download_eventconf_events     ({src_name})",
             c.download_eventconf_events, src_name, note=_ec_note)


def test_asset_suggestions(c):
    _section("asset suggestions")
    run("get_asset_suggestions", c.get_asset_suggestions)


def test_scv(c):
    _section("secure credentials vault")
    result = warn("get_credentials", c.get_credentials,
                  note="requires SCV REST API support")
    creds = []
    if isinstance(result, dict):
        creds = result.get("credential", [])
    elif isinstance(result, list):
        creds = result
    if creds:
        alias = creds[0] if isinstance(creds[0], str) else creds[0].get("alias")
        if alias:
            warn(f"get_credential  ({alias})", c.get_credential, alias,
                 note="requires SCV REST API support")


def test_config_mgmt(c):
    _section("configuration management")
    names_r = run("get_config_names", c.get_config_names)
    warn("get_config_schemas", c.get_config_schemas,
         note="may return empty body on some versions")
    cfg_names = names_r if isinstance(names_r, list) else []
    if cfg_names:
        cname = cfg_names[0]
        warn(f"get_config_schema  ({cname})", c.get_config_schema, cname,
             note="may return empty body on some versions")
        warn(f"get_config_ids     ({cname})", c.get_config_ids, cname,
             note="may return empty body on some versions")


def test_snmptrap_nbi(c):
    _section("SNMP trap NBI config")
    warn("get_snmptrap_nbi_config", c.get_snmptrap_nbi_config,
         note="requires SNMP trap NBI plugin")
    warn("get_snmptrap_nbi_status", c.get_snmptrap_nbi_status,
         note="requires SNMP trap NBI plugin")


def test_email_nbi(c):
    _section("email NBI config")
    warn("get_email_nbi_config", c.get_email_nbi_config,
         note="requires email NBI plugin")
    warn("get_email_nbi_status", c.get_email_nbi_status,
         note="requires email NBI plugin")


def test_syslog_nbi(c):
    _section("syslog NBI config")
    warn("get_syslog_nbi_config", c.get_syslog_nbi_config,
         note="requires syslog NBI plugin")
    warn("get_syslog_nbi_status", c.get_syslog_nbi_status,
         note="requires syslog NBI plugin")


def test_javamail_config(c):
    _section("javamail config")
    warn("get_javamail_default_config", c.get_javamail_default_config,
         note="may not be available on all versions")
    run("get_javamail_readmails", c.get_javamail_readmails)
    run("get_javamail_sendmails", c.get_javamail_sendmails)
    run("get_javamail_end2ends", c.get_javamail_end2ends)


def test_pagination(c):
    _section("pagination")
    # Paginate nodes with a tiny page size and verify we get the full count.
    total_r = run("get_node_count", c.get_node_count)
    if isinstance(total_r, int) and total_r > 0:
        cap = min(total_r, 15)  # don't fetch thousands
        items = []
        try:
            for node in c.paginate(c.get_nodes, "node", page_size=5):
                items.append(node)
                if len(items) >= cap:
                    break
            _ok(f"paginate(get_nodes, page_size=5)",
                f"{len(items)} items (cap {cap})")
        except Exception as exc:
            _fail("paginate(get_nodes, page_size=5)", exc)
    else:
        _skip("paginate(get_nodes)", "no nodes or count unavailable")


def test_exceptions(c):
    _section("exception hierarchy")
    # Verify that a 404 raises NotFoundError, not bare HTTPError.
    try:
        c.get_node(999999999)
        _fail("NotFoundError on missing node",
              "expected NotFoundError but call succeeded")
    except opennms.NotFoundError:
        _ok("NotFoundError on missing node",
            "get_node(999999999) raised NotFoundError")
    except Exception as exc:
        _fail("NotFoundError on missing node",
              f"expected NotFoundError, got {type(exc).__name__}: {exc}")


# ── Write-operation tests ──────────────────────────────────────────────────────

def test_write_ops(c):
    tag = f"smoke-{int(time.time())}"
    _section(f"write operations  [tag: {tag}]")

    # Events ── fire-and-forget; no cleanup needed
    run("create_event (internal test UEI)", c.create_event, {
        "uei": "uei.opennms.org/internal/test",
        "source": "smoke_test.py",
        "severity": "Normal",
        "parms": {"parm": [
            {"parmName": "smoke-tag", "value": {"content": tag}},
        ]},
    })

    # Alarms ── ack then immediately unack; only if an unacked alarm exists
    _, aid = _first(c.get_alarms, "alarm")
    if aid:
        try:
            alarm = c.get_alarm(aid)
            already_acked = isinstance(alarm, dict) and alarm.get("ackUser") is not None
        except Exception:
            already_acked = True  # play it safe
        if not already_acked:
            run(f"ack_alarm    id={aid}", c.ack_alarm, aid)
            run(f"unack_alarm  id={aid}", c.unack_alarm, aid)
        else:
            _skip(f"ack_alarm / unack_alarm  id={aid}",
                  "already acknowledged – skipping to avoid side-effects")
    else:
        _skip("ack_alarm / unack_alarm", "no alarms")

    # Categories ── create / get / delete
    cat_name = f"Smoke-Test-{tag}"
    r = run(f"create_category  ({cat_name})", c.create_category, {"name": cat_name})
    if r is not _FAILED:
        run(f"get_category     ({cat_name})", c.get_category, cat_name)
        run(f"delete_category  ({cat_name})", c.delete_category, cat_name)
    else:
        _skip(f"get_category / delete_category  ({cat_name})", "create failed")

    # Groups ── create / get / delete
    grp_name = f"smoke-test-{tag}"
    r = run(f"create_group  ({grp_name})", c.create_group,
            {"name": grp_name, "comments": "smoke test – safe to delete"})
    if r is not _FAILED:
        run(f"get_group     ({grp_name})", c.get_group, grp_name)
        run(f"delete_group  ({grp_name})", c.delete_group, grp_name)
    else:
        _skip(f"get_group / delete_group  ({grp_name})", "create failed")

    # Scheduled outages ── create / get / delete
    so_name = f"smoke-test-{tag}"
    r = run(f"create_sched_outage  ({so_name})", c.create_sched_outage, {
        "name": so_name,
        "type": "specific",
        "time": [{"begins": "01-Jan-2000 00:00:00", "ends": "01-Jan-2000 00:00:01"}],
    })
    if r is not _FAILED:
        run(f"get_sched_outage     ({so_name})", c.get_sched_outage, so_name)
        run(f"delete_sched_outage  ({so_name})", c.delete_sched_outage, so_name)
    else:
        _skip(f"get_sched_outage / delete_sched_outage  ({so_name})", "create failed")

    # Requisitions ── create / get / delete (no import, so no real nodes created)
    req_name = f"smoke-test-{tag}"
    r = run(f"create_requisition  ({req_name})", c.create_requisition,
            {"foreign-source": req_name, "node": []})
    if r is not _FAILED:
        run(f"get_requisition     ({req_name})", c.get_requisition, req_name)
        run(f"delete_requisition  ({req_name})", c.delete_requisition, req_name)
    else:
        _skip(f"get_requisition / delete_requisition  ({req_name})", "create failed")

    # Maps ── create / update / delete
    r = run("create_map", c.create_map,
            {"name": f"Smoke Test {tag}", "mapWidth": 1920, "mapHeight": 1080})
    mid = r.get("id") if isinstance(r, dict) else None
    if mid:
        run(f"update_map  id={mid}", c.update_map, mid,
            {"name": f"Smoke Test {tag} (updated)", "mapWidth": 1920, "mapHeight": 1080})
        run(f"delete_map  id={mid}", c.delete_map, mid)
    elif r is not _FAILED:
        _skip("update_map / delete_map", "create_map returned no id")
    else:
        _skip("update_map / delete_map", "create_map failed")


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Smoke-test the OpenNMS API wrapper against a live server.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "environment variables:\n"
            "  OPENNMS_URL         base URL (e.g. https://onms.example.com:8443)\n"
            "  OPENNMS_USER        username (rest role required)\n"
            "  OPENNMS_PASSWORD    password\n"
            "  OPENNMS_VERIFY_SSL  set to 'false' to skip SSL certificate verification\n"
            "  OPENNMS_TIMEOUT     request timeout in seconds (default: 60)\n"
        ),
    )
    parser.add_argument(
        "--write", action="store_true",
        help="Also exercise write operations (create/update/delete). "
             "Use in dev/staging only.",
    )
    parser.add_argument(
        "--yes", action="store_true",
        help="Skip the write-mode confirmation prompt (for CI pipelines).",
    )
    parser.add_argument(
        "--no-color", action="store_true",
        help="Disable ANSI colour output.",
    )
    parser.add_argument(
        "--skip", type=str, default="",
        help="Comma-separated list of test label prefixes to skip. "
             "E.g. --skip get_resources,get_flow",
    )
    args = parser.parse_args()

    global _skip_prefixes
    if args.skip:
        _skip_prefixes = [s.strip() for s in args.skip.split(",") if s.strip()]

    url      = os.environ.get("OPENNMS_URL")
    user     = os.environ.get("OPENNMS_USER")
    password = os.environ.get("OPENNMS_PASSWORD")
    verify   = os.environ.get("OPENNMS_VERIFY_SSL", "true").lower() != "false"
    timeout  = int(os.environ.get("OPENNMS_TIMEOUT", "60"))

    missing = [name for name, val in
               [("OPENNMS_URL", url), ("OPENNMS_USER", user),
                ("OPENNMS_PASSWORD", password)]
               if not val]
    if missing:
        sys.exit(f"Error: missing environment variable(s): {', '.join(missing)}")

    if args.write and not args.yes:
        print("\n  WARNING: Write mode will create and delete objects on the server.")
        print("  Operations that will mutate server state:")
        print("    create_event, ack_alarm/unack_alarm, category CRUD,")
        print("    group CRUD, scheduled outage CRUD, requisition CRUD, map CRUD")
        print("  All created objects are deleted at the end of the run.")
        print("  ONLY use against a dev or staging server -- NEVER production.")
        print(f"\n  Target URL: {url}")
        confirm = input("\n  Type 'yes' to continue: ").strip()
        if confirm.lower() != "yes":
            sys.exit("Aborted.")
        print()

    if args.no_color:
        import builtins
        _real_print = builtins.print
        def _plain(*a, **kw):
            text = " ".join(str(x) for x in a)
            builtins.print = _real_print          # avoid recursion
            _real_print(re.sub(r"\033\[[0-9;]*m", "", text), **kw)
            builtins.print = _plain
        builtins.print = _plain

    client = opennms.OpenNMS(url=url, username=user, password=password,
                             verify_ssl=verify, timeout=timeout)

    print("OpenNMS Smoke Test")
    print(f"  URL:  {url}")
    print(f"  User: {user}")
    print(f"  Mode: {'read + write' if args.write else 'read-only (getters)'}")
    if not verify:
        print("  SSL:  verification disabled")

    test_info(client)
    test_alarms(client)
    test_events(client)
    test_acks(client)
    test_notifications(client)
    test_nodes(client)
    test_outages(client)
    test_requisitions(client)
    test_foreign_sources(client)
    test_snmp_config(client)
    test_groups(client)
    test_users(client)
    test_categories(client)
    test_sched_outages(client)
    test_ksc_reports(client)
    test_resources(client)
    test_measurements(client)
    test_heatmap(client)
    test_maps(client)
    test_graphs(client)
    test_flows(client)
    test_device_config(client)
    test_situations(client)
    test_business_services(client)
    test_enlinkd(client)
    test_v2_interfaces(client)
    test_monitoring_locations(client)
    test_minions(client)
    test_ifservices(client)
    test_availability(client)
    test_health(client)
    test_whoami(client)
    test_monitoring_systems(client)
    test_prefab_graphs(client)
    test_flow_dscp(client)
    test_business_service_functions(client)
    test_classifications(client)
    test_situation_feedback(client)
    test_user_defined_links(client)
    test_applications(client)
    test_perspective_poller(client)
    test_foreign_sources_config(client)
    test_requisition_names(client)
    test_snmp_metadata(client)
    test_provisiond(client)
    test_eventconf(client)
    test_asset_suggestions(client)
    test_scv(client)
    test_config_mgmt(client)
    test_snmptrap_nbi(client)
    test_email_nbi(client)
    test_syslog_nbi(client)
    test_javamail_config(client)
    test_pagination(client)
    test_exceptions(client)

    if args.write:
        test_write_ops(client)

    total = _passed + _failed + _warned + _skipped
    print(f"\n{'─' * 56}")
    parts = [f"{_passed} passed", f"{_failed} failed"]
    if _warned:
        parts.append(f"{_warned} warned")
    parts.append(f"{_skipped} skipped")
    print(f"  {'  ·  '.join(parts)}  ({total} total)")

    if _warnings:
        print("\nWarnings (non-fatal):")
        for label, err in _warnings:
            print(f"  {label}")
            print(f"    {err}")

    if _failures:
        print("\nFailures:")
        for label, err in _failures:
            print(f"  {label}")
            print(f"    {err}")

    sys.exit(0 if _failed == 0 else 1)


if __name__ == "__main__":
    main()
