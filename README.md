# opennms-api-wrapper

[![CI](https://github.com/cnewkirk/opennms-api-wrapper/actions/workflows/ci.yml/badge.svg)](https://github.com/cnewkirk/opennms-api-wrapper/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/cnewkirk/opennms-api-wrapper/graph/badge.svg)](https://codecov.io/gh/cnewkirk/opennms-api-wrapper)
[![PyPI](https://img.shields.io/pypi/v/opennms-api-wrapper)](https://pypi.org/project/opennms-api-wrapper/)
[![Docs](https://readthedocs.org/projects/opennms-api-wrapper/badge/?version=stable)](https://opennms-api-wrapper.readthedocs.io/en/stable/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An unofficial, dependency-minimal Python 3 client for the
[OpenNMS](https://www.opennms.com/) REST API (Horizon 30+ and
Meridian). 100% coverage of the Meridian 2025 REST API reference,
live-validated read and write — see [Compatibility](#compatibility).

> **OpenNMS resources**: [Docs](https://docs.opennms.com/) ·
> [REST API reference](https://docs.opennms.com/horizon/latest/development/rest/rest-api.html) ·
> [Community forum](https://opennms.discourse.group/)

**[Full API reference →](https://opennms-api-wrapper.readthedocs.io/en/stable/api/)**

## Features

- Covers every v1 (`/opennms/rest/`) and v2 (`/opennms/api/v2/`) endpoint
- Plain dicts in, plain dicts out — the few endpoints that require XML
  or form-encoded bodies are handled internally
- Single runtime dependency: [`requests`](https://docs.python-requests.org/)
- Synchronous and straightforward — no async complexity
- `TypedDict` schemas for all write payloads — field names, types, and docs in your IDE
- Typed exception hierarchy — catch `NotFoundError`, `ForbiddenError`, etc. without importing `requests`
- Pagination helper — `client.paginate()` yields all items from any list endpoint automatically
- Full test suite with method coverage (mocked HTTP — no live server required)
- Read and write smoke tests live-validated against the Meridian 2025 foundation

## Installation

```bash
pip install opennms-api-wrapper
```

**From source** (latest development version):

```bash
git clone https://github.com/cnewkirk/opennms-api-wrapper.git
cd opennms-api-wrapper
pip install .
```

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
| Maps | full CRUD + map elements (pre-Horizon 16 servers only — API removed upstream) |
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
| Status (v2) | severity summaries + filterable lists for nodes/applications/business services |
| Outage timelines | header, image, empty, HTML |
| Reports | templates, run, persisted, scheduled, download |
| Search (v2) | global context search |
| GraphML | get, create, delete |
| Grafana endpoints | CRUD, verify, dashboards |
| Geocoding (v2) | config, geocoders, activate, configure |
| Geolocation (v2) | tile-server config, node location query |
| Logs | list files, file contents |
| Filesystem | list, extensions, help, contents CRUD |
| Data choices | usage stats report/status/meta, product update |
| News feed (v2) | latest items |

## Compatibility

**Certified coverage baseline: OpenNMS Meridian 2025.** This library
covers 100% of the resource areas in the
[Meridian 2025 REST API reference](https://docs.opennms.com/meridian/2025/development/rest/rest-api.html)
apart from the three web-UI-internal APIs (Menu, Web Assets,
UI Extension) — 66 of 69 documented areas. `COVERAGE.md` has the full
matrix. Read and write paths are smoke-tested against the Meridian
2025 foundation build (`opennms/horizon:foundation-2025`,
Horizon 34.0.1) via `tests/live/compose.yaml`.

**Expected server range: Horizon 30+ and corresponding Meridian
releases.** The v1 write contracts this library speaks (XML creates,
form-encoded updates, per the OpenNMS REST docs) are stable across
versions, and the JSON-first endpoints rely on JSON support present
since Horizon 30. Horizon releases before 30 are end-of-life and not
supported. Only the certified baseline above is verified by live
testing; reports from other versions are welcome.

**Per-method version exceptions** (also noted in the affected
docstrings):

- Event configuration (`/api/v2/eventconf`) requires Horizon 35+.
- Maps (`/rest/maps`) was removed upstream in Horizon 16; those
  methods only function on pre-16 servers.

Validation history: 0.4.5 was smoke-tested read-only against Meridian
2024.3.0; 0.5.0 is smoke-tested read and write against the Meridian
2025 foundation.

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
as a substitute for the mocked unit suite.

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
categories, groups, requisitions, etc.).  It will prompt for explicit
confirmation and print the target URL before running a single write.
**Only use write mode against a dev or staging instance — never
production.** The throwaway instance in `tests/live/compose.yaml` is a
safe target.

```bash
python smoke_test.py --write          # interactive prompt required
python smoke_test.py --write --yes    # skip prompt (CI pipelines only)
python smoke_test.py --no-color       # plain output for log files
python smoke_test.py --skip get_resources,get_flow  # skip slow tests
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

Bug reports and pull requests are welcome on
[GitHub](https://github.com/cnewkirk/opennms-api-wrapper).

## Acknowledgements

All API shapes are derived from the official
[OpenNMS](https://www.opennms.com/) REST API documentation.

[requests](https://docs.python-requests.org/) handles all HTTP communication.
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/) renders the
documentation site.

[GitHub](https://github.com/), [Read the Docs](https://readthedocs.org/), and
[PyPI](https://pypi.org/) generously provide source hosting, CI, versioned
docs, and package distribution free of charge for open source projects.
