#!/usr/bin/env python3
"""
smoke_test.py – Exercise the OpenNMS API wrapper against a live server.

Read-only mode (default) is safe to run against any server, including
production.  It issues only GET requests and makes no changes.

Write mode (--write) creates and deletes objects on the server.  It will
prompt for explicit confirmation before running.  Only use write mode against
a dev or staging instance — never against production.

Environment variables (all required):
    OPENNMS_URL         Base URL, e.g. "https://opennms.example.com:8443"
    OPENNMS_USER        OpenNMS username (needs at minimum the ``rest`` role)
    OPENNMS_PASSWORD    Password
    OPENNMS_VERIFY_SSL  Set to "false" to disable SSL verification (default: true)

Usage:
    python smoke_test.py                 # read-only — safe for any server
    python smoke_test.py --write         # write ops — prompts for confirmation
    python smoke_test.py --write --yes   # write ops — skip prompt (CI only)
    python smoke_test.py --no-color      # plain output for log files
"""

import argparse
import os
import re
import sys
import time

import opennms_api_wrapper as opennms


# ── Output ─────────────────────────────────────────────────────────────────────

_passed = _failed = _skipped = 0
_failures: list = []

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


def run(label: str, fn, *args, detail_fn=None, **kwargs):
    """Call *fn* and record PASS or FAIL.

    Returns the call's return value, or ``_FAILED`` if an exception was raised.
    """
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
    run("get_alarm_count",         c.get_alarm_count,
        detail_fn=lambda r: str(r))
    run("get_alarm_stats",         c.get_alarm_stats)
    run("get_alarm_stats_by_severity", c.get_alarm_stats_by_severity)
    run("get_alarm_history",       c.get_alarm_history)
    run("get_alarms_v2",           c.get_alarms_v2, limit=5,
        detail_fn=lambda r: _n(r, "alarm"))

    _, aid = _first(c.get_alarms, "alarm")
    if aid:
        run(f"get_alarm                id={aid}", c.get_alarm, aid,
            detail_fn=lambda r: r.get("severity", "") if isinstance(r, dict) else "")
        run(f"get_alarm_v2             id={aid}", c.get_alarm_v2, aid)
        run(f"get_alarm_history_at     id={aid}", c.get_alarm_history_at, aid)
        run(f"get_alarm_history_states id={aid}", c.get_alarm_history_states, aid)
    else:
        for lbl in ("get_alarm", "get_alarm_v2",
                    "get_alarm_history_at", "get_alarm_history_states"):
            _skip(lbl, "no alarms")


def test_events(c):
    _section("events")
    run("get_events",      c.get_events, limit=5, detail_fn=lambda r: _n(r, "event"))
    run("get_event_count", c.get_event_count, detail_fn=lambda r: str(r))

    _, eid = _first(c.get_events, "event")
    if eid:
        run(f"get_event  id={eid}", c.get_event, eid)
    else:
        _skip("get_event", "no events")


def test_acks(c):
    _section("acknowledgements")
    run("get_acks",      c.get_acks, limit=5,
        detail_fn=lambda r: _n(r, "ack"))
    run("get_ack_count", c.get_ack_count, detail_fn=lambda r: str(r))

    _, ack_id = _first(c.get_acks, "ack")
    if ack_id:
        run(f"get_ack  id={ack_id}", c.get_ack, ack_id)
    else:
        _skip("get_ack", "no acks")


def test_notifications(c):
    _section("notifications")
    run("get_notifications",      c.get_notifications, limit=5,
        detail_fn=lambda r: _n(r, "notification"))
    run("get_notification_count", c.get_notification_count,
        detail_fn=lambda r: str(r))

    _, nid = _first(c.get_notifications, "notification")
    if nid:
        run(f"get_notification  id={nid}", c.get_notification, nid)
    else:
        _skip("get_notification", "no notifications")


def test_nodes(c):
    _section("nodes")
    run("get_nodes",      c.get_nodes, limit=5, detail_fn=lambda r: _n(r, "node"))
    run("get_node_count", c.get_node_count, detail_fn=lambda r: str(r))

    _, nid = _first(c.get_nodes, "node")
    if nid:
        run(f"get_node                    id={nid}", c.get_node, nid,
            detail_fn=lambda r: r.get("label", "") if isinstance(r, dict) else "")
        run(f"get_node_ip_interfaces      id={nid}", c.get_node_ip_interfaces,
            nid, limit=3, detail_fn=lambda r: _n(r, "ipInterface"))
        run(f"get_node_snmp_interfaces    id={nid}", c.get_node_snmp_interfaces,
            nid, limit=3, detail_fn=lambda r: _n(r, "snmpInterface"))
        run(f"get_node_categories         id={nid}", c.get_node_categories, nid)
        run(f"get_node_asset_record       id={nid}", c.get_node_asset_record, nid)
        run(f"get_node_hardware_inventory id={nid}", c.get_node_hardware_inventory, nid)
        run(f"get_node_metadata           id={nid}", c.get_node_metadata, nid)
        run(f"get_node_outages            id={nid}", c.get_node_outages, nid)
        run(f"get_resources_for_node      id={nid}", c.get_resources_for_node, str(nid))
    else:
        for lbl in ("get_node", "get_node_ip_interfaces", "get_node_snmp_interfaces",
                    "get_node_categories", "get_node_asset_record",
                    "get_node_hardware_inventory", "get_node_metadata",
                    "get_node_outages", "get_resources_for_node"):
            _skip(lbl, "no nodes")


def test_outages(c):
    _section("outages")
    run("get_outages",      c.get_outages, limit=5,
        detail_fn=lambda r: _n(r, "outage"))
    run("get_outage_count", c.get_outage_count, detail_fn=lambda r: str(r))

    _, oid = _first(c.get_outages, "outage")
    if oid:
        run(f"get_outage  id={oid}", c.get_outage, oid)
    else:
        _skip("get_outage", "no outages")


def test_requisitions(c):
    _section("requisitions")
    run("get_requisitions",               c.get_requisitions,
        detail_fn=lambda r: _n(r, "model-import"))
    run("get_requisition_count",          c.get_requisition_count,
        detail_fn=lambda r: str(r))
    run("get_deployed_requisitions",      c.get_deployed_requisitions,
        detail_fn=lambda r: _n(r, "model-import"))
    run("get_deployed_requisition_count", c.get_deployed_requisition_count,
        detail_fn=lambda r: str(r))


def test_foreign_sources(c):
    _section("foreign sources")
    run("get_foreign_sources",              c.get_foreign_sources)
    run("get_deployed_foreign_sources",     c.get_deployed_foreign_sources)
    run("get_deployed_foreign_source_count", c.get_deployed_foreign_source_count,
        detail_fn=lambda r: str(r))
    run("get_default_foreign_source",       c.get_default_foreign_source)


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
    run("get_ksc_reports",      c.get_ksc_reports,
        detail_fn=lambda r: _n(r, "kscReport"))
    run("get_ksc_report_count", c.get_ksc_report_count,
        detail_fn=lambda r: str(r))


def test_resources(c):
    _section("resources")
    run("get_resources", c.get_resources, depth=1)


def test_heatmap(c):
    _section("heatmap")
    run("get_heatmap_outages_categories",         c.get_heatmap_outages_categories)
    run("get_heatmap_outages_foreign_sources",    c.get_heatmap_outages_foreign_sources)
    run("get_heatmap_outages_monitored_services", c.get_heatmap_outages_monitored_services)
    run("get_heatmap_alarms_categories",          c.get_heatmap_alarms_categories)
    run("get_heatmap_alarms_foreign_sources",     c.get_heatmap_alarms_foreign_sources)
    run("get_heatmap_alarms_monitored_services",  c.get_heatmap_alarms_monitored_services)


def test_maps(c):
    _section("maps")
    result = run("get_maps", c.get_maps, detail_fn=lambda r: _n(r, "map"))
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
    run("get_flow_count",     c.get_flow_count, detail_fn=lambda r: str(r))
    run("get_flow_exporters", c.get_flow_exporters,
        detail_fn=lambda r: _n(r, "exporters"))
    # These may legitimately fail if no flow data has been ingested.
    run("get_flow_applications",           c.get_flow_applications, top_n=5)
    run("get_flow_applications_enumerate", c.get_flow_applications_enumerate, limit=5)
    run("get_flow_conversations",          c.get_flow_conversations, top_n=5)
    run("get_flow_conversations_enumerate",c.get_flow_conversations_enumerate, limit=5)
    run("get_flow_hosts",                  c.get_flow_hosts, top_n=5)
    run("get_flow_hosts_enumerate",        c.get_flow_hosts_enumerate, limit=5)


def test_device_config(c):
    _section("device config")
    run("get_device_configs",        c.get_device_configs, limit=5,
        detail_fn=lambda r: _n(r, "deviceConfig"))
    run("get_latest_device_configs", c.get_latest_device_configs, limit=5,
        detail_fn=lambda r: _n(r, "deviceConfig"))


def test_situations(c):
    _section("situations (v2)")
    run("get_situations", c.get_situations, limit=5,
        detail_fn=lambda r: _n(r, "alarm"))


def test_business_services(c):
    _section("business services (v2)")
    run("get_business_services", c.get_business_services,
        detail_fn=lambda r: _n(r, "business-service"))


def test_v2_interfaces(c):
    _section("ip/snmp interfaces (v2)")
    run("get_ip_interfaces",   c.get_ip_interfaces, limit=5,
        detail_fn=lambda r: _n(r, "ipInterface"))
    run("get_snmp_interfaces", c.get_snmp_interfaces, limit=5,
        detail_fn=lambda r: _n(r, "snmpInterface"))


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
    args = parser.parse_args()

    url      = os.environ.get("OPENNMS_URL")
    user     = os.environ.get("OPENNMS_USER")
    password = os.environ.get("OPENNMS_PASSWORD")
    verify   = os.environ.get("OPENNMS_VERIFY_SSL", "true").lower() != "false"

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
                             verify_ssl=verify)

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
    test_heatmap(client)
    test_maps(client)
    test_graphs(client)
    test_flows(client)
    test_device_config(client)
    test_situations(client)
    test_business_services(client)
    test_v2_interfaces(client)

    if args.write:
        test_write_ops(client)

    total = _passed + _failed + _skipped
    print(f"\n{'─' * 56}")
    print(f"  {_passed} passed  ·  {_failed} failed  ·  {_skipped} skipped"
          f"  ({total} total)")

    if _failures:
        print("\nFailures:")
        for label, err in _failures:
            print(f"  {label}")
            print(f"    {err}")

    sys.exit(0 if _failed == 0 else 1)


if __name__ == "__main__":
    main()
