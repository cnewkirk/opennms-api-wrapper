# opennms-api-wrapper

[![CI](https://github.com/cnewkirk/opennms-api-wrapper/actions/workflows/ci.yml/badge.svg)](https://github.com/cnewkirk/opennms-api-wrapper/actions/workflows/ci.yml)
[![GitHub release](https://img.shields.io/github/v/release/cnewkirk/opennms-api-wrapper)](https://github.com/cnewkirk/opennms-api-wrapper/releases)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A thin, dependency-minimal Python 3 wrapper for the
[OpenNMS](https://www.opennms.com/) REST API (Horizon 35+).
Validated against OpenNMS Meridian 2024.3.0 with a live-server smoke test
suite.

**[Full API reference →](https://cnewkirk.github.io/opennms-api-wrapper/api/)**

## Features

- Covers every v1 (`/opennms/rest/`) and v2 (`/opennms/api/v2/`) endpoint
- JSON everywhere — no XML handling required
- Single runtime dependency: [`requests`](https://docs.python-requests.org/)
- Synchronous and straightforward — no async complexity
- `TypedDict` schemas for all write payloads — field names, types, and docs in your IDE
- Typed exception hierarchy — catch `NotFoundError`, `ForbiddenError`, etc. without importing `requests`
- Pagination helper — `client.paginate()` yields all items from any list endpoint automatically
- 478-test suite with full method coverage (mocked HTTP — no live server required)
- Live-server smoke test validated against Meridian 2024.3.0

## Installation

**From the GitHub release** (no clone required — recommended for most users):

```bash
pip install https://github.com/cnewkirk/opennms-api-wrapper/archive/refs/tags/v0.3.1.tar.gz
```

**From source** (clone first, then install):

```bash
git clone https://github.com/cnewkirk/opennms-api-wrapper.git
cd opennms-api-wrapper
pip install .
```

When the package is published to PyPI, installation will simplify to
`pip install opennms-api-wrapper`.

## Quick start

```python
import opennms_api_wrapper as opennms

client = opennms.OpenNMS(
    url="https://opennms.example.com:8443",
    username="admin",
    password="admin",
)

# Server info
info = client.get_info()
print(info["displayVersion"])

# List alarms
alarms = client.get_alarms(limit=25, order_by="lastEventTime", order="desc")
for alarm in alarms["alarm"]:
    print(alarm["id"], alarm["severity"], alarm["nodeLabel"])

# Acknowledge an alarm
client.ack_alarm(alarm_id=42)

# List alarms with FIQL filter (v2)
alarms = client.get_alarms_v2(fiql="severity==MAJOR")
```

## Error handling

HTTP errors raise typed exceptions — no need to import `requests`:

```python
import opennms_api_wrapper as opennms

try:
    node = client.get_node(99999)
except opennms.NotFoundError:
    print("Node does not exist")
except opennms.ForbiddenError:
    print("Insufficient permissions")
except opennms.AuthenticationError:
    print("Check your credentials")
except opennms.OpenNMSError:
    print("Unexpected error")
```

Full hierarchy: `OpenNMSHTTPError` (base, exposes `.status_code` and
`.response`) → `BadRequestError` (400), `AuthenticationError` (401),
`ForbiddenError` (403), `NotFoundError` (404), `ConflictError` (409),
`ServerError` (5xx).

## Pagination

`client.paginate()` transparently handles `limit`/`offset` pagination and
yields individual items:

```python
# Fetch every MAJOR alarm — no manual offset loop required
for alarm in client.paginate(client.get_alarms, "alarm", severity="MAJOR"):
    print(alarm["id"], alarm["nodeLabel"])

# Works with any list endpoint
for node in client.paginate(client.get_nodes, "node"):
    print(node["id"], node["label"])
```

The optional `page_size` argument (default 100) controls how many items are
fetched per request.

## API coverage

| Resource group | Methods |
|---|---|
| Alarms (v1 + v2) | list, get, count, ack/unack/clear/escalate, bulk ops |
| Alarm statistics | stats, stats by severity |
| Alarm history | history, history at timestamp, state changes |
| Events | list, get, count, create, ack/unack, bulk ack/unack |
| Nodes | full CRUD + IP interfaces, SNMP interfaces, services, categories, assets, hardware |
| Outages | list, get, count, node outages |
| Notifications | list, get, count, trigger destination path |
| Acknowledgements | list, get, count, create, ack/unack notification |
| Requisitions | full CRUD including nodes, interfaces, services, categories, assets |
| Foreign sources | full CRUD including detectors and policies |
| SNMP configuration | get, set |
| Groups | full CRUD + user and category membership |
| Users | full CRUD + role assignment |
| Categories | full CRUD + node and group associations |
| Scheduled outages | full CRUD + daemon associations |
| KSC reports | list, get, count, create, update |
| Resources | list, get, get for node, select, delete |
| Measurements | single attribute (GET), multi-source (POST) |
| Heatmap | outages + alarms × categories / foreign sources / services / nodes |
| Maps | full CRUD + map elements |
| Topology graphs | containers, graph, graph view (POST), search suggestions, search results |
| Flows | count, exporters, applications, conversations, hosts |
| Device configuration | list, get, get by interface, latest, download, backup |
| Situations (v2) | list, create, add alarms, clear, accept, remove alarms |
| Business services (v2) | full CRUD |
| Metadata (v2) | full CRUD for node, interface, and service metadata |
| Server info | get |
| Discovery (v2) | submit scan configuration |
| IP interfaces (v2) | list with FIQL |
| SNMP interfaces (v2) | list with FIQL |
| EnLinkd (v2) | aggregate, LLDP/CDP/OSPF/IS-IS/Bridge links and elements |
| Monitoring locations | list, get, default, count, create, update, delete |
| Minions | list, get, count |
| If services | list (v1), update (v1), list with FIQL (v2) |
| Availability | summary, by category, by node, per-category-node |
| Health | health check, probe |
| Whoami | current user info |
| Classifications | rules CRUD, groups CRUD, classify, protocols, CSV import |
| Situation feedback | tags, get/submit feedback |
| User-defined links (v2) | list, get, create, delete |
| Applications (v2) | list, get, create, delete |
| Perspective poller (v2) | application status, service status |
| Foreign sources config | policies, detectors, services, assets, categories |
| Requisition names | list all names |
| SNMP metadata (v2) | get by node |
| Provisiond (v2) | daemon status, job status |
| Event configuration (v2) | filter, sources, CRUD, upload, enable/disable, vendors |
| Monitoring systems | main system info |
| Asset suggestions | field suggestions |
| Secure credentials vault | full CRUD |
| Configuration management | names, schemas, config CRUD, sub-parts |
| SNMP trap NBI config | config, status, trap sink CRUD |
| Email NBI config | config, status, destination CRUD |
| Syslog NBI config | config, status, destination CRUD |
| Javamail config | defaults, readmails/sendmails/end2ends CRUD |

## Authentication

Basic authentication is used. Pass `verify_ssl=False` to disable certificate
verification (useful for self-signed certs in lab environments):

```python
client = opennms.OpenNMS(
    url="https://opennms.example.com:8443",
    username="admin",
    password="admin",
    verify_ssl=False,
)
```

## Smoke testing

`smoke_test.py` exercises the wrapper against a real OpenNMS server.  It is
intended for use against a dev or staging instance before each release — not
as a substitute for the 463-test mocked unit suite.

Tests that depend on optional plugins or heavy endpoints are reported as
**WARN** (non-fatal) rather than FAIL.  Each warning includes the specific
plugin or feature required.

**Read-only mode** (default) is safe to run against any server, including
production.  It issues only GET requests and makes no changes.

```bash
export OPENNMS_URL="https://opennms.example.com:8443"
export OPENNMS_USER="admin"
export OPENNMS_PASSWORD="secret"
export OPENNMS_VERIFY_SSL="false"   # omit or set to "true" for valid certs
export OPENNMS_TIMEOUT="60"         # per-request timeout in seconds (default 60)

python smoke_test.py
```

**Write mode** creates and then deletes objects on the server (events,
categories, groups, requisitions, maps, etc.).  It will prompt for explicit
confirmation and print the target URL before running a single write.
**Only use write mode against a dev or staging instance — never production.**

```bash
python smoke_test.py --write          # interactive prompt required
python smoke_test.py --write --yes    # skip prompt (CI pipelines only)
python smoke_test.py --no-color       # plain output for log files
python smoke_test.py --skip get_resources --skip get_flow  # skip slow tests
```

The `--skip` flag accepts a prefix — `--skip get_flow` skips all tests
whose label starts with `get_flow`.

## Development

```bash
git clone https://github.com/cnewkirk/opennms-api-wrapper.git
cd opennms-api-wrapper
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## Contributing

Bug reports and pull requests are welcome on GitHub at
https://github.com/cnewkirk/opennms-api-wrapper.

## Acknowledgements

This library was designed and tested by a human, with implementation
assistance from [Claude Code](https://claude.ai/code) (Anthropic). All API
shapes are derived from the official OpenNMS Horizon 35 REST API
documentation.
